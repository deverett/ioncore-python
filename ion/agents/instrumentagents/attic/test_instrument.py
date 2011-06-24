#!/usr/bin/env python

"""
@file ion/agents/instrumentagents/test/test_instrument.py
@brief This test file should test logic that is common across various
    instrument agent classes. This might include registration, lifecycle
    set/get, etc. It may use a specific class as an example, but
    the tests should reflect the larger features that are mostly implemented
    by the InstrumentAgent class.
@author Michael Meisinger
@author Stephen Pasco
@author Steve Foley
"""
'''
import ion.util.ionlog
log = ion.util.ionlog.getLogger(__name__)
from twisted.internet import defer

from ion.data.dataobject import LCStates as LCS
from ion.test.iontest import IonTestCase
from ion.agents.instrumentagents import instrument_agent as IA
from ion.services.coi.agent_registry import AgentRegistryClient
from ion.resources.ipaa_resource_descriptions import InstrumentAgentResourceInstance
from ion.resources.dm_resource_descriptions import SubscriptionResource
from ion.agents.instrumentagents.SBE49_constants import ci_commands as IACICommands
from ion.agents.instrumentagents.SBE49_constants import ci_parameters as IACIParameters
from ion.agents.instrumentagents.SBE49_constants import instrument_commands as IAInstCommands
from ion.agents.instrumentagents.SBE49_constants import instrument_parameters as IAInstParameters
from ion.agents.instrumentagents.simulators.sim_SBE49 import Simulator
from ion.core.exception import ReceivedError
import ion.util.procutils as pu
from twisted.trial import unittest

class TestInstrumentAgent(IonTestCase):

    @defer.inlineCallbacks
    def setUp(self):
        
        
        yield self._start_container()




        """
        # startup a simulator
        self.simulator = Simulator("123", 9000)
        self.SimulatorPort = self.simulator.start()
        self.assertNotEqual(self.SimulatorPort, 0)
        
        # Start an instrument agent
        processes = [
            {'name':'pubsub_service','module':'ion.services.dm.distribution.pubsub_service','class':'PubSubService'},
            {'name':'agent_registry',
             'module':'ion.services.coi.agent_registry',
             'class':'AgentRegistryService'},
            {'name':'testSBE49IA',
             'module':'ion.agents.instrumentagents.SBE49_IA',
             'class':'SBE49InstrumentAgent'}
        ]
        self.sup = yield self._spawn_processes(processes)
        self.svc_id = yield self.sup.get_child_id('testSBE49IA')
        self.reg_id = yield self.sup.get_child_id('agent_registry')

        # Start a client (for the RPC)
        self.IAClient = IA.InstrumentAgentClient(proc=self.sup,
                                                 target=self.svc_id)

        # Start an Agent Registry to test against
        self.reg_client = AgentRegistryClient(proc=self.sup)
        yield self.reg_client.clear_registry()
        """
    @defer.inlineCallbacks
    def tearDown(self):
        
        """
        yield self.simulator.stop()
        
        #child_id = yield self.sup.get_child_id('pubsub_service')
        #pubsub = self._get_procinstance(child_id)
        #pubsub.reg.clear_registry()
        
        
        yield pu.asleep(1)
        """
        yield self._stop_container()
        

    @defer.inlineCallbacks
    def test_get_SBE49_capabilities(self):
        """
        Test the ability to gather capabilities from the SBE49 instrument
        capabilities
        """
        raise unittest.SkipTest("InstrumentAgent rewrite in progress.")
        
        result = yield self.IAClient.get_capabilities()
        #log.info("getCapabilities result: "+ str(result))
        self.assert_(set(IACIParameters).issubset(set(result[IA.ci_parameters])))
        self.assert_(IA.driver_address in
                     result[IA.ci_parameters])
        self.assert_(list(IACICommands) == result[IA.ci_commands])
        self.assert_(list(IAInstCommands) ==
                     result[IA.instrument_commands])
        self.assert_(list(IAInstParameters) ==
                     result[IA.instrument_parameters])

    @defer.inlineCallbacks
    def test_get_set_SBE49_params(self):
        """
        Test the ability of the SBE49 driver to send and receive get, set,
        and other messages. Best called as RPC message pairs.
        """
        raise unittest.SkipTest("InstrumentAgent rewrite in progress.")
        
        response = yield self.IAClient.get_from_instrument(['baudrate',
                                                                'outputformat'])
        self.assertEqual(response['baudrate'], 9600)
        self.assertEqual(response['outputformat'], 0)

        response = yield self.IAClient.set_to_instrument({'baudrate': 19200,
                                            'outputformat': 1})
        self.assertEqual(response['baudrate'], 19200)
        self.assertEqual(response['outputformat'], 1)

        response = yield self.IAClient.get_from_instrument(['baudrate',
                                                            'outputformat'])
        self.assertEqual(response['baudrate'], 19200)
        self.assertEqual(response['outputformat'], 1)

        response = yield self.IAClient.set_to_instrument({'outputformat': 2})
        self.assertEqual(response['outputformat'], 2)

        # Try setting something bad
        try:
            response = yield self.IAClient.set_to_instrument({'baudrate': 19200,
                                                'badvalue': 1})
            self.fail("ReceivedError expected")
        except ReceivedError:
            log.debug("Correctly caught a ReceivedError")

        
    @defer.inlineCallbacks
    def test_registration(self):
        """
        Tests the ability of an instrument agent to successfully register
        ifself with the resource registry.
        """
        raise unittest.SkipTest("InstrumentAgent rewrite in progress.")
        
        reg_ref = yield self.IAClient.register_resource("123")

        result = yield self.IAClient.get_resource_instance()
        self.assertNotEqual(result, None)

        self.assert_(isinstance(result, InstrumentAgentResourceInstance))
        self.assertNotEqual(result.driver_process_id, None)
        self.assertEqual(result.instrument_ref.RegistryIdentity, "123")

        self.assertEqual(reg_ref.RegistryCommit, '')
        self.assertNotEqual(result.RegistryCommit, reg_ref.RegistryCommit)
        self.assertEqual(reg_ref.RegistryIdentity, result.RegistryIdentity)

        # Verify the reference is the same
        result = yield self.IAClient.get_resource_ref()

        self.assertEqual(result, reg_ref)

    @defer.inlineCallbacks
    def test_lifecycle_states(self):
        """
        Test the resource lifecycle management
        """
        raise unittest.SkipTest("InstrumentAgent rewrite in progress.")
        
        yield self.IAClient.register_resource("123")

        response = yield self.IAClient.set_lifecycle_state(LCS.inactive)
        self.assertEqual(response, LCS.inactive)

        response = yield self.IAClient.get_lifecycle_state()
        self.assertEqual(response, LCS.inactive)
        self.assertNotEqual(response, LCS.active)

        response = yield self.IAClient.set_lifecycle_state(LCS.active)
        self.assertEqual(response, LCS.active)

        response = yield self.IAClient.get_lifecycle_state()
        self.assertEqual(response, LCS.active)

        
    @defer.inlineCallbacks
    def test_execute_device(self):
        """
        Test the ability of the SBE49 driver to execute commands through the
        InstrumentAgentClient class
        """
        raise unittest.SkipTest('InstrumentAgent rewrite in progress.')

        response = yield self.IAClient.execute_device(['start', 'now', 1])
        log.debug("response: %s " % response)
        self.assert_(isinstance(response, dict))
        self.assert_('start' in response['value'])
        #self.assert_('stop' in response['value'])
        yield pu.asleep(3)

        try:
            response = yield self.IAClient.execute_device(['badcommand',
                                                            'now','1'])
            self.fail("ReceivedError expected")
        except ReceivedError:
            pass

        try:
            response = yield self.IAClient.execute_device([])
            self.fail("ReceivedError expected")
        except ReceivedError:
            pass

    @defer.inlineCallbacks
    def test_get_driver_proc(self):
        """
        Test the methods for retreiving the driver process directly from
        the instrument agent.
        """
        raise unittest.SkipTest('InstrumentAgent rewrite in progress.')
        
        
        response = yield self.IAClient.get_observatory([IA.driver_address])
        self.assertNotEqual(response, None)
        """
        Not the best test or logic, but see if the format is at least close
        Need a better way to get at the process id of the driver...maybe
        out of the registry?
        """
        self.assertEqual(str(response[IA.driver_address]).rsplit('.', 1)[0],
                         str(self.svc_id).rsplit('.', 1)[0])

    @defer.inlineCallbacks
    def test_status(self):
        """
        Test to see if the status response is correct
        @todo Do we even need this function?
        """
        raise unittest.SkipTest('InstrumentAgent rewrite in progress.')
        
        
        response = yield self.IAClient.get_status(['some_arg'])
        self.assert_(isinstance(response, dict))
        self.assertEqual(response['InstrumentState'], 'a-ok')

    @defer.inlineCallbacks
    def test_execute_observatory_phrase(self):
        raise unittest.SkipTest("Driver and test don't match return values")
        """
        Test the ability to manipulate phrases in an instrument agent
        """
        
        raise unittest.SkipTest('InstrumentAgent rewrite in progress.')
        
        
        try:
            response = yield self.IAClient.end_phrase()
            self.fail("ReceivedError expected")
        except ReceivedError:
            pass
        
        # Make a phrase to test start/cancel
        result = yield self.IAClient.start_phrase(5)
        print "result = "
        print result
        self.assertEqual(result['status'], "OK")
        yield self.IAClient.execute_observatory(['StateTransition', 'Reset'])
        yield self.IAClient.execute_observatory(['StateTransition', 'GoActive'])
        try:
            response = yield self.IAClient.start_phrase()
            self.fail("ReceivedError expected")
        except ReceivedError:
            pass
        result = yield self.IAClient.cancel_phrase()
        self.assertEqual(result['status'], "OK")
        try:
            response = yield self.IAClient.cancel_phrase()
            self.fail("ReceivedError expected")
        except ReceivedError:
            pass
        
        # Make a new one to test end
        result = yield self.IAClient.start_phrase()        
        self.assertEqual(result['status'], "OK")
        yield self.IAClient.execute_observatory(['StateTransition', 'Reset'])
        yield self.IAClient.execute_observatory(['StateTransition', 'GoActive'])
        result = yield self.IAClient.end_phrase()
        self.assertEqual(result['status'], "OK")

        try:
            response = yield self.IAClient.end_phrase()
            self.fail("ReceivedError expected")
        except ReceivedError:
            pass

        try:
            response = yield self.IAClient.start_phrase()
            self.fail("ReceivedError expected")
        except ReceivedError:
            pass

'''