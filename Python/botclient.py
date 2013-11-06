import sys
import json

from multiprocessing import Process, Queue, Value
from twisted.internet import protocol, reactor
from twisted.protocols import basic
import botprotocol, relayprotocol

filename='userdb'   #json formatted as {token: user, ...}
patha='placeholder1'
pathb='placeholder2'
commandq=Queue()    #contains items in format (user, field, data)

class BotRelayFactory(protocol.ServerFactory):
    protocol=relayprotocol.RelayProtocol

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

reactora.listenTCP(6667, BotFactory())
reactorb.listenTCP(6668, BotRelayFactory())
reactorc.listenTCP(6669, BotRelayFactory())
reactora.run()
reactorb.run()
reactorc.run()
