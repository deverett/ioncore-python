#!/usr/bin/env python

"""
@file ion/services/cei/provisioner_core.py
@author David LaBissoniere
@brief Starts, stops, and tracks instance and context state.
"""

import os
import logging
logging = logging.getLogger(__name__)
from itertools import izip
from twisted.internet import defer, threads

from nimboss.node import NimbusNodeDriver
from nimboss.ctx import ContextClient, BrokerError
from nimboss.cluster import ClusterDriver
from nimboss.nimbus import NimbusClusterDocument, ValidationError
from libcloud.types import NodeState as NimbossNodeState
from libcloud.base import Node as NimbossNode
from libcloud.drivers.ec2 import EC2NodeDriver
from ion.services.cei.provisioner_store import group_records, calc_record_age
from ion.services.cei.dtrs import DeployableTypeLookupError
from ion.services.cei import states
from ion.services.cei import cei_events

__all__ = ['ProvisionerCore', 'ProvisioningError']

_NIMBOSS_STATE_MAP = {
        NimbossNodeState.RUNNING : states.STARTED, 
        NimbossNodeState.REBOOTING : states.STARTED, #TODO hmm
        NimbossNodeState.PENDING : states.PENDING,
        NimbossNodeState.TERMINATED : states.TERMINATED,
        NimbossNodeState.UNKNOWN : states.ERROR_RETRYING}

# Window of time in which nodes are allowed to be launched 
# but not returned in queries to the IaaS. After this, nodes
# are assumed to be terminated out of band and marked FAILED
_IAAS_NODE_QUERY_WINDOW_SECONDS = 60

class ProvisionerCore(object):
    """Provisioner functionality that is not specific to the service.
    """

    def __init__(self, store, notifier, dtrs, context=None):
        self.store = store
        self.notifier = notifier
        self.dtrs = dtrs

        #TODO how about a config file
        nimbus_key = os.environ['NIMBUS_KEY']
        nimbus_secret = os.environ['NIMBUS_SECRET']
        nimbus_test_driver = NimbusNodeDriver(nimbus_key, secret=nimbus_secret,
                host='nimbus.ci.uchicago.edu', port=8444)
        nimbus_uc_driver = NimbusNodeDriver(nimbus_key, secret=nimbus_secret,
                host='tp-vm1.ci.uchicago.edu', port=8445)
       
        ec2_key = os.environ['AWS_ACCESS_KEY_ID']
        ec2_secret = os.environ['AWS_SECRET_ACCESS_KEY']
        ec2_east_driver = EC2NodeDriver(ec2_key, ec2_secret)

        self.node_drivers = {
                'nimbus-test' : nimbus_test_driver,
                'nimbus-uc' : nimbus_uc_driver,
                'ec2-east' : ec2_east_driver,
                }
        
        self.context = context or ProvisionerContextClient(
                'https://nimbus.ci.uchicago.edu:8888/ContextBroker/ctx/', 
                nimbus_key, nimbus_secret)
        
        self.cluster_driver = ClusterDriver()

    @defer.inlineCallbacks
    def prepare_provision(self, request):
        """Validates request and commits to datastore.

        If the request has subscribers, they are notified with the
        node state records.

        If the request is invalid and doesn't contain enough information
        to notify subscribers via normal channels, a ProvisioningError
        is raised. This is almost certainly a client programming error.
        
        If the request is well-formed but invalid, for example if the 
        deployable type does not exist in the DTRS, FAILED records are 
        recorded in data store and subscribers are notified.

        Returns a tuple (launch record, node records).
        """

        try:
            deployable_type = request['deployable_type']
            launch_id = request['launch_id']
            subscribers = request['subscribers']
            nodes = request['nodes']
        except KeyError,e:
            raise ProvisioningError('Invalid request. Missing key: ' + str(e))

        if not (isinstance(nodes, dict) and len(nodes) > 0):
            raise ProvisioningError('Invalid request. nodes must be a non-empty dict')

        # optional variables to sub into ctx document template
        vars = request.get('vars')

        #validate nodes and build DTRS request
        dtrs_nodes = {}
        for node_name, node in nodes.iteritems():
            try:
                dtrs_nodes[node_name] = {
                        'count' : len(node['ids']),
                        'site' : node['site'], 
                        'allocation' : node['allocation']}
            except (KeyError, ValueError):
                raise ProvisioningError('Invalid request. Node %s spec is invalid' % 
                        node_name)
        
        # from this point on, errors result in failure records, not exceptions.
        # except for, you know, bugs.
        state = states.REQUESTED
        state_description = None
        try:
            dt = yield self.dtrs.lookup(deployable_type, dtrs_nodes, vars)
            document = dt['document']
            dtrs_nodes = dt['nodes']
            logging.debug('got dtrs nodes: ' + str(dtrs_nodes))
        except DeployableTypeLookupError, e:
            logging.error('Failed to lookup deployable type "%s" in DTRS: %s', 
                    deployable_type, str(e))
            state = states.FAILED
            state_description = "DTRS_LOOKUP_FAILED " + str(e)

        launch_record = {
                'launch_id' : launch_id,
                'document' : document,
                'deployable_type' : deployable_type,
                'subscribers' : subscribers,
                'state' : state}

        node_records = []
        for (group_name, group) in nodes.iteritems():
            node_ids = group['ids']
            for node_id in node_ids:
                record = {'launch_id' : launch_id,
                        'node_id' : node_id,
                        'state' : state,
                        'state_desc' : state_description,
                        'site' : group['site'],
                        'allocation' : group['allocation'],
                        'ctx_name' : group_name,
                        }
                #DTRS returns a bunch of IaaS specific info:
                # ssh key name, "real" allocation name, etc.
                # we fold it in blindly
                record.update(dtrs_nodes[group_name])
                node_records.append(record)

        yield self.store.put_record(launch_record)
        yield self.store_and_notify(node_records, subscribers)

        defer.returnValue((launch_record, node_records))

    @defer.inlineCallbacks
    def execute_provision(self, launch, nodes):
        """Brings a launch to the PENDING state.

        Any errors or problems will result in FAILURE states
        which will be recorded in datastore and sent to subscribers.
        """
    
        error_state = None
        error_description = None
        try: 
            yield self._really_execute_provision_request(launch, nodes)
        
        except ProvisioningError, e:
            logging.error('Failed to execute launch. Problem: ' + str(e))
            error_state = states.FAILED
            error_description = e.message
        
        except Exception, e: # catch all exceptions, need to ensure nodes are marked FAILED
            logging.error('Launch failed due to an unexpected error. '+
                    'This is likely a bug and should be reported. Problem: ' + 
                    str(e))
            error_state = states.FAILED
            error_description = 'PROGRAMMER_ERROR '+str(e)
        
        if error_state:
            launch['state'] = error_state
            launch['state_desc'] = error_description

            for node in nodes:
                node['state'] = error_state
                node['state_desc'] = error_description

            #store and notify launch and nodes with FAILED states
            yield self.store.put_record(launch)
            yield self.store_and_notify(nodes, launch['subscribers'], error_state)
    
    @defer.inlineCallbacks
    def _really_execute_provision_request(self, launch, nodes):
        """Brings a launch to the PENDING state.
        """

        subscribers = launch['subscribers']
        docstr = launch['document']

        try:
            doc = NimbusClusterDocument(docstr)
        except ValidationError, e:
            raise ProvisioningError('CONTEXT_DOC_INVALID '+str(e))
        
        launch_groups = group_records(nodes, 'ctx_name')
        
        context = None
        if doc.needs_contextualization:
            try:
                context = yield self.context.create()
            except BrokerError, e:
                raise ProvisioningError('CONTEXT_CREATE_FAILED ' + str(e))

            logging.debug('Created new context: ' + context.uri)
            launch['context'] = context
            
            yield self.store.put_record(launch, states.PENDING)
        
        else:
            raise ProvisioningError('NOT_IMPLEMENTED launches without contextualization '+
                    'unsupported')
        
        cluster = self.cluster_driver.new_bare_cluster(context.uri)
        specs = doc.build_specs(context)

        # we want to fail early, before we launch anything if possible
        launch_pairs = self._validate_launch_groups(launch_groups, specs)

        #launch_pairs is a list of (spec, node list) tuples
        for launch_spec, launch_nodes in launch_pairs:
            newstate = None
            try:
                yield self._launch_one_group(launch_spec, launch_nodes, cluster)
            
            except Exception,e:
                logging.exception('Problem launching group %s: %s', 
                        launch_spec.name, str(e))
                newstate = states.FAILED
                # should we have a backout of earlier groups here? or just leave it up
                # to EPU controller to decide what to do?
            
            yield self.store_and_notify(launch_nodes, subscribers, newstate)

    def _validate_launch_groups(self, groups, specs):
        if len(specs) != len(groups):
            raise ProvisioningError('INVALID_REQUEST group count mismatch '+
                    'between cluster document and request')
        pairs = []
        for spec in specs:
            group = groups.get(spec.name)
            if not group:
                raise ProvisioningError('INVALID_REQUEST missing \''+ spec.name +
                        '\' node group, present in cluster document')
            if spec.count != len(group):
                raise ProvisioningError('INVALID_REQUEST node group \''+ 
                        spec.name + '\' specifies ' + len(group) + 
                        ' nodes, but cluster document has '+ spec.count)
            pairs.append((spec, group))
        return pairs

    @defer.inlineCallbacks
    def _launch_one_group(self, spec, nodes, cluster):
        """Launches a single group: a single IaaS request.
        """

        #assumption here is that a launch group does not span sites or
        #allocations. That may be a feature for later.

        one_node = nodes[0]
        site = one_node['site']
        driver = self.node_drivers[site]
        
        #set some extras in the spec
        allocation = one_node.get('iaas_allocation')
        if allocation:
            spec.size = allocation
        sshkeyname = one_node.get('iaas_sshkeyname')
        if sshkeyname:
            spec.keyname = sshkeyname

        logging.debug('Launching group %s - %s nodes (keypair=%s)', 
                spec.name, spec.count, spec.keyname)
        
        try:
            iaas_nodes = yield threads.deferToThread(
                    self.cluster_driver.launch_node_spec, spec, driver)
        except Exception, e:
            logging.exception('Error launching nodes: ' + str(e))
            # wrap this up?
            raise
        
        cluster.add_node(iaas_nodes)

        # underlying node driver may return a list or an object
        if not hasattr(iaas_nodes, '__iter__'):
            iaas_nodes = [iaas_nodes]

        if len(iaas_nodes) != len(nodes):
            message = '%s nodes from IaaS launch but %s were expected' % (
                    len(iaas_nodes), len(nodes))
            logging.error(message)
            raise ProvisioningError('IAAS_PROBLEM '+ message)
            
        for node_rec, iaas_node in izip(nodes, iaas_nodes):
            node_rec['iaas_id'] = iaas_node.id
            # for some reason, ec2 libcloud driver places IP in a list
            #TODO if we support drivers that actually have multiple
            #public and private IPs, we will need to revist this
            public_ip = iaas_node.public_ip
            if isinstance(public_ip, list):
                public_ip = public_ip[0]
            private_ip = iaas_node.private_ip
            if isinstance(private_ip, list):
                private_ip = private_ip[0]
            node_rec['public_ip'] = public_ip
            node_rec['private_ip'] = private_ip
            node_rec['extra'] = iaas_node.extra.copy()
            node_rec['state'] = states.PENDING
            
            extradict = {'public_ip': public_ip, 'iaas_id': iaas_node.id}
            cei_events.event("provisioner", "new_node", 
                             logging, extra=extradict)
    
    @defer.inlineCallbacks
    def store_and_notify(self, records, subscribers, newstate=None):
        """Convenience method to store records and notify subscribers.
        """
        yield self.store.put_records(records, newstate)
        yield self.notifier.send_records(records, subscribers)

    @defer.inlineCallbacks
    def query_nodes(self, request):
        """Performs querys of IaaS and broker, sends updates to subscribers.
        """
        # Right now we just query everything. Could be made more granular later

        for site in self.node_drivers.iterkeys():
            nodes = yield self.store.get_site_nodes(site, 
                    before_state=states.TERMINATED)
            if nodes:
                yield self.query_one_site(site, nodes)

        yield self.query_contexts()

    @defer.inlineCallbacks
    def query_one_site(self, site, nodes, driver=None):
        node_driver = driver or self.node_drivers[site]

        logging.info('Querying site "%s"', site)
        nimboss_nodes = yield threads.deferToThread(node_driver.list_nodes)
        nimboss_nodes = dict((node.id, node) for node in nimboss_nodes)

        # note we are walking the nodes from datastore, NOT from nimboss
        for node in nodes:
            state = node['state']
            if state < states.PENDING or state >= states.TERMINATED:
                continue
            
            nimboss_id = node.get('iaas_id')
            nimboss_node = nimboss_nodes.pop(nimboss_id, None)
            if not nimboss_node:
                # this state is unknown to underlying IaaS. What could have
                # happened? IaaS error? Recovery from loss of net to IaaS?
                
                # Or lazily-updated records. On EC2, there can be a short
                # window where pending instances are not included in query
                # response

                if calc_record_age(node) <= _IAAS_NODE_QUERY_WINDOW_SECONDS:
                    logging.debug('node %s: not in query of IaaS, but within '+
                            'allowed startup window (%d seconds)',
                            node['node_id'], _IAAS_NODE_QUERY_WINDOW_SECONDS)
                else:
                    logging.warn('node %s: in data store but unknown to IaaS. '+
                            'Marking as terminated.', node['node_id'])

                    node['state'] = states.FAILED
                    node['state_desc'] = 'NODE_DISAPPEARED'

                    launch = yield self.store.get_launch(node['launch_id'])
                    yield self.store_and_notify([node], launch['subscribers'])
            else:
                nimboss_state = _NIMBOSS_STATE_MAP[nimboss_node.state]
                if nimboss_state > node['state']:
                    #TODO nimboss could go backwards in state.
                    node['state'] = nimboss_state
                    
                    public_ip = nimboss_node.public_ip
                    if isinstance(public_ip, list):
                        public_ip = public_ip[0]
                    private_ip = nimboss_node.private_ip
                    if isinstance(private_ip, list):
                        private_ip = private_ip[0]
                    node['public_ip'] = public_ip
                    node['private_ip'] = private_ip
                    
                    launch = yield self.store.get_launch(node['launch_id'])
                    yield self.store_and_notify([node], launch['subscribers'])
        #TODO nimboss_nodes now contains any other running instances that
        # are unknown to the datastore (or were started after the query)
        # Could do some analysis of these nodes

    @defer.inlineCallbacks
    def query_contexts(self):
        """Queries all open launch contexts and sends node updates.
        """
        #grab all the launches in the pending state
        launches = yield self.store.get_launches(state=states.PENDING)

        for launch in launches:
            context = launch.get('context')
            launch_id = launch['launch_id']
            if not context:
                logging.warn('Launch %s is in %s state but it has no context!',
                        launch['launch_id'], launch['state'])
                continue
            
            ctx_uri = context['uri']
            logging.debug('Querying context %s for launch %s ', ctx_uri, launch_id)
            context_status = yield self.context.query(ctx_uri)
            
            ctx_nodes = context_status.nodes
            if not ctx_nodes:
                logging.debug('Launch %s context has no nodes (yet)', launch_id)
                continue

            nodes = yield self.store.get_launch_nodes(launch_id)
            updated_nodes = update_nodes_from_context(nodes, ctx_nodes)

            if updated_nodes:
                logging.debug("%d nodes need to be updated as a result of the context query" % 
                        len(updated_nodes))
                yield self.store_and_notify(updated_nodes, launch['subscribers'])
            
            if context_status.complete:
                logging.info('Launch %s context is complete!', launch_id)
                # update the launch record so this context won't be re-queried
                launch['state'] = states.RUNNING
                yield self.store.put_record(launch)
            else:
                logging.debug('Launch %s context is incomplete: %s of %s nodes',
                        launch_id, len(context_status.nodes), 
                        context_status.expected_count)
    
    @defer.inlineCallbacks
    def mark_launch_terminating(self, launch_id):
        """Mark a launch as Terminating in data store.
        """
        launch = yield self.store.get_launch(launch_id)
        nodes = yield self.store.get_launch_nodes(launch_id)
        yield self.store_and_notify(nodes, launch['subscribers'], 
                states.TERMINATING)
    
    @defer.inlineCallbacks
    def terminate_launch(self, launch_id):
        """Destroy all nodes in a launch and mark as terminated in store.
        """
        launch = yield self.store.get_launch(launch_id)
        nodes = yield self.store.get_launch_nodes(launch_id)

        for node in nodes:
            state = node['state']
            if state < states.PENDING or state >= states.TERMINATED:
                continue
            #would be nice to do this as a batch operation
            yield self._terminate_node(node, launch)
            
    @defer.inlineCallbacks
    def terminate_launches(self, launch_ids):
        """Destroy all node in a set of launches.
        """
        for launch in launch_ids:
            yield self.terminate_launch(launch)

    @defer.inlineCallbacks
    def terminate_nodes(self, node_ids):
        """Destroy all specified nodes.
        """
        nodes = yield self.store.get_nodes_by_id(node_ids)
        for node_id, node in izip(node_ids, nodes):
            if not node:
                #maybe an error should make it's way to controller from here?
                logging.warn('Node %s unknown but requested for termination',
                        node_id)
                continue
            launch = yield self.store.get_launch(node['launch_id'])
            yield self._terminate_node(node, launch)
            
    @defer.inlineCallbacks
    def _terminate_node(self, node, launch):
        nimboss_node = self._to_nimboss_node(node)
        driver = self.node_drivers[node['site']]
        yield threads.deferToThread(driver.destroy_node, nimboss_node)
    
        yield self.store_and_notify([node], launch['subscribers'], 
                states.TERMINATED)

    def _to_nimboss_node(self, node):
        """Nimboss drivers need a Node object for termination.
        """
        #TODO this is unfortunately tightly coupled with EC2 libcloud driver
        # right now. We are building a fake Node object that only has the
        # attribute needed for termination (id). Would need to be fleshed out
        # to work with other drivers.
        return NimbossNode(id=node['iaas_id'], name=None, state=None,
                public_ip=None, private_ip=None, 
                driver=self.node_drivers[node['site']])

def update_nodes_from_context(nodes, ctx_nodes):
    updated_nodes = []
    for ctx_node in ctx_nodes:
        for ident in ctx_node.identities:

            match_reason = None
            match_node = None
            for node in nodes:
                if ident.ip and ident.ip == node['public_ip']:
                    match_node = node
                    match_reason = 'public IP match'
                    break
                elif ident.hostname and ident.hostname == node['public_ip']:
                    match_node = node
                    match_reason = 'nimboss IP matches ctx hostname'
                # can add more matches if needed

            if match_node:
                logging.debug('Matched ctx identity to node by: ' + match_reason)
                
                if _update_one_node_from_ctx(match_node, ctx_node, ident):
                    updated_nodes.append(match_node)
                    break

            else:
                # this isn't necessarily an exceptional condition. could be a private
                # IP for example. Right now we are only matching against public
                logging.debug('Context identity has unknown IP (%s) and hostname (%s)', 
                        ident.ip, ident.hostname)
    return updated_nodes

def _update_one_node_from_ctx(node, ctx_node, identity):
    node_done = ctx_node.ok_occurred or ctx_node.error_occurred
    if not node_done or node['state'] >= states.RUNNING:
        logging.debug('bail '+node['state'])
        return False
    if ctx_node.ok_occurred:
        node['state'] = states.RUNNING
        node['pubkey'] = identity.pubkey
    else:
        node['state'] = states.FAILED
        node['error_code'] = ctx_node.error_code
        node['error_message'] = ctx_node.error_message
    return True

class ProvisionerContextClient(object):
    """Provisioner calls to context broker.
    """
    def __init__(self, broker_uri, key, secret):
        self.client = ContextClient(broker_uri, key, secret)

    def create(self):
        """Creates a new context with the broker
        """
        return threads.deferToThread(self.client.create_context)

    def query(self, resource):
        """Queries an existing context.

        resource is the uri returned by create operation
        """
        return threads.deferToThread(self.client.get_status, resource)


class ProvisioningError(Exception):
    pass
