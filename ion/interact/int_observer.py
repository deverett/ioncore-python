#!/usr/bin/env python

"""
@file ion/interact/int_observer.py
@author Michael Meisinger
@author Dave Foster <dfoster@asascience.com>
@brief A process that observes interactions in the Exchange
"""
import string

from twisted.internet import defer

import ion.util.ionlog
log = ion.util.ionlog.getLogger(__name__)

from ion.core.messaging.receiver import FanoutReceiver
from ion.core.process.process import Process, ProcessFactory
import ion.util.procutils as pu
import re
from ion.services.dm.distribution.events import EventSubscriber

class InteractionObserver(Process):
    """
    @brief Process that observes ongoing interactions in the Exchange. Logs
        them to disk and makes them available in the local container (for
        testing) and on request.
    """


    def __init__(self, *args, **kwargs):
        """
        """
        Process.__init__(self, *args, **kwargs)

        self.max_msglog = 3000
        self.msg_log = []
        self.write_on_term = True

        # Create a receiver (inbound queue consumer) for service name
        self.msg_receiver = FanoutReceiver(
                name='#',
                label='InteractionObserver',
                process=self,
                handler=self.msg_receive)
        self.add_receiver(self.msg_receiver)

        self.ev_sub = EventSubscriber(process=self)
        self.ev_sub.ondata = self.ev_receive

        self.add_life_cycle_object(self.msg_receiver)
        self.add_life_cycle_object(self.ev_sub)

    @defer.inlineCallbacks
    def plc_terminate(self):
        #yield self.msg_receiver.deactivate()
        #yield self.msg_receiver.terminate()
        if self.write_on_term:
            f = open('msc.txt', 'w')
            f.write(self.writeout_msc())
            f.close()

    @defer.inlineCallbacks
    def msg_receive(self, payload, msg):
        self.log_message(payload)
        yield msg.ack()

    def ev_receive(self, evmsg):
        self.log_message(evmsg, True)



    def log_message(self, hdrs, evmsg=False):
        """
        @param evmsg    This message is an event, render it as such!
        """
        mhdrs = hdrs.copy()

        if isinstance(mhdrs['content'], ion.core.messaging.message_client.MessageInstance):
            mclass = mhdrs['content'].__class__.__name__.split('MessageInstance_')[-1]
            if 'Wrapper_' in mclass:
                mclass = string.replace(mclass, "Wrapper_", "")
        else:
            mclass = mhdrs['content'].__class__.__name__

        # lose the content, we don't want to hold it, but store its type name
        mhdrs.pop('content', None)
        mhdrs['_content_type'] = mclass

        # TUPLE: timestamp (MS), type, boolean if its an event
        msg_rec = (pu.currenttime_ms(), mhdrs, evmsg)
        self.msg_log.append(msg_rec)

        #log.debug(mhdrs)

        hstr = "MSG %d: %s(%s) -> %s %s:%s:%s-%s; uid=%s, status=%s" % (msg_rec[0],
                mhdrs.get('sender',None),
                mhdrs.get('sender-name',None),
                mhdrs.get('receiver',None), mhdrs.get('protocol',None),
                mhdrs.get('performative',None), mhdrs.get('op',None), mhdrs.get('conv-seq',None),
                mhdrs.get('user-id',None), mhdrs.get('status',None))

        log.info(hstr)

        # Truncate if too long in increments of 100
        if len(self.msg_log) > self.max_msglog + 100:
            self.msg_log = self.msg_log[100:]

    def writeout_msc(self):
        msglog = self.msg_log[:]
        procs = []
        senders = []
        proc_alias = {}     # maps receivers -> process names
        open_rpcs = {}      # maps convid -> unknown receiver names

        for msgtup in msglog:
            msg = msgtup[1]
            sid = msg.get('sender', '??')
            rec = msg.get('receiver')
            sname = msg.get('sender-name', sid)

            # map sender to process name
            if not sid in proc_alias:
                proc_alias[sid] = sname

            # is this rpc?
            if msg.get('protocol', None) == 'rpc':

                # if this is a request, do we know who it is addressed to?
                performative = msg.get('performative', None)
                convid = msg.get('conv-id', None)

                if convid is None or performative is None:
                    log.warn('Intercepted message with no performative or convid, but says it is rpc')
                elif performative == 'request':
                    torec = msg.get('receiver', None)
                    if torec is not None and torec not in proc_alias:
                        # add to open rpc conversation maps
                        open_rpcs[convid] = torec
                        log.debug("Adding receiver %s to open conversations to resolve (conv id %s)" % (torec, convid))

                elif performative != 'timeout':     # all other items are responses, so we should be able to get info

                    # have we seen this conversation before and need to resolve a receiver name?
                    if convid in open_rpcs:
                        oldrecname = open_rpcs.pop(convid)
                        proc_alias[oldrecname] = msg.get('sender-name', oldrecname)

                        log.debug("Mapping receiver %s to proc name %s" % (oldrecname, proc_alias[oldrecname]))
                else:
                    # @TODO: timeout? we never see it
                    pass

            # catch any non-rpc leftover destinations, make sure they are not events, we do not want their destinations
            # as a line in the msc!
            if not rec in procs and not msgtup[2]:
                procs.append(rec)


        # senders are - anything in the proc_alias values or the open_rpcs values as we've not resolved them
        senders.extend(set(proc_alias.itervalues()))    # proc_alias values contain many duplicates, reduce them
        senders.extend(open_rpcs.itervalues())

        # add leftover non-rpc destinations
        for rec in procs:
            if not (rec in proc_alias or rec in open_rpcs.values()):
                senders.append(rec)

        def sanitize(input):
            return string.replace(string.replace(input, ".", "_"), "-", "_")

        msc = "msc {\n"
        msc += ' wordwraparcs="1";\n'
        sstr = sanitize(",".join(senders))
        msc += " %s;\n" % sstr

        for msgtup in msglog:
            msg = msgtup[1]

            sid = msg.get('sender', '??')
            sname = proc_alias.get(sid, sid)
            sname = sanitize(sname)

            rec = msg.get('receiver')

            rname = proc_alias.get(rec, rec)
            rname = sanitize(rname)

            if msgtup[2]:
                # this is an EVENT, show it as a box!
                evlabel = "%s" % (rname)

                msc += ' %s abox %s [ label="%s", textbgcolor="orange" ];\n' % (sname, sname, evlabel)
            else:

                #mlabel = "%s:%s:%s:%s" % (msg.get('protocol',None),
                #    msg.get('performative',None), msg.get('op',None), msg.get('conv-seq',None))
                # @todo Clean up sender and receiver names - remove host and PID
                #re.sub('.+:','',sname)

                mlabel = "%s\\n(%s->%s)\\n<%s>" % (msg.get('op', None), sid.rsplit(".", 1)[-1], rec.rsplit(".", 1)[-1], msg.get('_content_type', ''))

                # default attributes: only a label
                attrs = {'label': mlabel}

                # determine arrow type used based on message type
                arrow = '->'
                if msg.get('protocol', None) == 'rpc':

                    # we know its rpc based on arrow type and color, so we change the label to be more friendly
                    #rpclabel = "%s (%s->%s) <%s>" % (msg.get('op', None), sid.rsplit(".", 1)[-1], rec.rsplit(".", 1)[-1], msg.get('_content_type', ''))
                    #attrs['label'] = rpclabel

                    arrow = ">>"    # default response, covers a few cases here

                    performative = msg.get('performative', None)
                    if performative == 'request':
                        arrow = '=>'
                    elif performative == 'timeout':
                        arrow = '-x'    # timeout, unfortunatly you don't see this as it never gets messaged, @TODO

                    if performative == 'failure' or performative == 'error':
                        attrs['textbgcolor'] = 'red'
                        attrs['linecolor'] = 'red'
                    else:
                        attrs['textcolor'] = 'navy'
                        attrs['linecolor'] = 'navy'
                else:
                    # non rpc -> perhaps a data message for ingest/exgest?
                    #msglabel = "%s (%s->%s) <%s>"
                    pass

                msc += ' %s %s %s [ %s ];\n' % (sname, arrow, rname, ','.join(('%s="%s"' % (k, v) for k,v in attrs.iteritems())))

        msc += "}\n"

        return msc



# Spawn off the process using the module name
factory = ProcessFactory(InteractionObserver)


class InteractionMonitor(InteractionObserver):
    """
    @brief Extension of the InteractionObserver that observes interactions of
        a specific process and monitors it for correctness.
    @note The tricky thing is to relate incoming and outgoing messages of a
        process.
    """


class ConversationMonitor(InteractionObserver):
    """
    @brief Extension of the InteractionMonitor that distinguishes and monitors
        conversations within the interactions of a specific for correctness.
        Such conversations need to comply to a conversation type, which must
        be specified in an electronic format (such as Scribble, FSM) that can
        be operationally enacted (i.e. followed message by message)
    """
