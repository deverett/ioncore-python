#!/usr/bin/env python

"""
@file ion/services/hello_service.py
@author Michael Meisinger
@brief  example service definition that can be used as template
"""

import logging
from twisted.internet import defer
from magnet.spawnable import Receiver

import ion.util.procutils as pu
from ion.services.base_service import BaseService, BaseServiceClient, RpcClient

logging.basicConfig(level=logging.DEBUG)
logging.debug('Loaded: '+__name__)

class HelloService(BaseService):
    """Example service implementation
    """
    
    def __init__(self, receiver):
        BaseService.__init__(self, receiver)
        logging.info('HelloService.__init__()')

    def slc_init(self):
        pass

    @defer.inlineCallbacks
    def op_hello(self, content, headers, msg):
        logging.info('op_hello: '+str(content))
        
        replyto = msg.reply_to
        if replyto != None and replyto != '':
            yield self.send_message(pu.get_process_id(replyto), 'reply', {'value':'Hello there, '+str(content)}, {})
        else:
            logging.info('op_hello: Cannot send reply. No reply_to given')


class HelloServiceClient(RpcClient):

    @defer.inlineCallbacks
    def hello(self, to='1', text='Hi there'):
        cont = yield self.rpc_send(to, 'hello', text, {})
        logging.info('Friends reply: '+str(cont))

# Direct start of the service as a process with its default name
receiver = Receiver(__name__)
instance = HelloService(receiver)


"""
from ion.services import hello_service as h
spawn(h)
send(1, {'op':'hello','content':'Hello you there!'})

from ion.services.hello_service import HelloServiceClient
hc = HelloServiceClient()
hc.spawnClient()
hc.hello()
"""
