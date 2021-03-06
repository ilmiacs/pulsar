'''Test the Pulsar Client in pulsar.async.mailbox'''
import time
import socket

import pulsar
from pulsar.apps.test import unittest

# you need to pass functions, you cannot pass lambdas
def testrun(actor):
    return actor.aid


class ClientMixin:
    
    def client(self):
        actor = pulsar.get_actor()
        arbiter = actor.arbiter
        c = pulsar.PulsarClient.connect(arbiter.address)
        self.assertFalse(c.async)
        m = actor.arbiter.mailbox
        # They are two clients of the arbiter mailbox
        self.assertEqual(c.remote_address, m.remote_address)
        self.assertNotEqual(c.address, m.address)
        return c
    
    
class TestPulsarClient(unittest.TestCase, ClientMixin):
    
    def testPing(self):
        c = self.client()
        self.assertEqual(c.ping(), 'pong')
        self.assertEqual(c.received, 1)
        self.assertEqual(c.ping(), 'pong')
        self.assertEqual(c.received, 2)
        actor = pulsar.get_actor()
        
    def testEcho(self):
        c = self.client()
        self.assertEqual(c.echo('Hello!'), 'Hello!')
        self.assertEqual(c.echo('Ciao!'), 'Ciao!')
        self.assertEqual(c.received, 2)
        
    def testInfo(self):
        c = self.client()
        info = c.info()
        self.assertTrue(info)
        self.assertTrue(len(info['monitors']) >= 1)
        
        
class TestClosePulsarClient(unittest.TestCase, ClientMixin):
    
    def testQuit(self):
        c = self.client()
        self.assertEqual(c.ping(), 'pong')
        self.assertRaises(socket.error, c.quit)
        self.assertRaises(socket.error, c.ping)
        
    def testClose(self):
        #TODO
        #This is a bad test in multiprocessing mode
        c = self.client()
        info = c.info()
        connections1 = info['server']['internal_connections']
        c2 = self.client()
        info = c2.info()
        connections2 = info['server']['internal_connections']
        # This is a bad test in multiprocessing mode
        #self.assertEqual(connections1+1, connections2)
        # lets drop one
        c.close()
        # give it some time
        time.sleep(0.2)
        info = c2.info()
        connections3 = info['server']['internal_connections']
        #self.assertEqual(connections1, connections3)