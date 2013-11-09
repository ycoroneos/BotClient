import sys
import json

from multiprocessing import Process, Queue, Value
from twisted.internet import protocol, reactor
from twisted.protocols import basic
import botprotocol, relayprotocol

filename='userdb.json'   #json formatted as {token: user, ...}

class BotRelayFactory(protocol.ServerFactory):
    protocol=relayprotocol.BotRelayProtocol

    def __init__(self):
        self.connected=False
        self.targetuser=None

    def isconnected(self):
        return self.connected

    def connect(self):
        self.connected=True

    def disconnect(self):
        self.connected=False

    def settargetuser(self, user):
        self.targetuser=user

    def gettargetuser(self):
        return self.targetuser

class BotFactory(protocol.ServerFactory):
    protocol = botprotocol.BotProtocol

    def __init__(self):
        self.connections=0
        self.db=json.loads(open(filename, 'r').read())

    def addConnection(self):
        self.connections+=1

    def removeConnection(self):
        self.connections-=1

    def check_token(self, token):
        if (token in self.db):
            return self.db[token]
        return False

reactor.listenTCP(6667, BotFactory())
reactor.listenTCP(6668, BotRelayFactory())
#reactorc.listenTCP(6669, BotRelayFactory())
reactor.run()
#reactorc.run()
