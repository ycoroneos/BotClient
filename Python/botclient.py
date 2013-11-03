import sys
import json
import socket
sys.path.append(r'modules/')

from twisted.internet import protocol, reactor
from twisted.protocols import basic
import botprotocol

filename='userdb'   #json formatted as {token: user, ...}
patha='placeholder1'
pathb='placeholder2'

class BotFactory(protocol.ServerFactory):
    protocol = botprotocol.BotProtocol

    def __init__(self):
        self.connections=0
        self.db=json.loads(open(filename, 'r').read())
        self.socka=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socka.connect(patha)
        self.sockb=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sockb.connect(pathb)

    def addConnection(self):
        self.connections+=1

    def removeConnection(self):
        self.connections-=1

    def check_token(self, token):
        if (token in self.db):
            return True
        return False

    def write_socket(self, data):
        pass

reactor.listenTCP(6667, BotFactory())
reactor.run()
