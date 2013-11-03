from twisted.internet import protocol, reactor
from twisted.protocols import basic
import json

class BotProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.factory.addConnection()

    def connectionLost(self, reason):
        self.factory.removeConnection()

    def lineReceived(self, line):
        data=json.loads(line)
        if (self.factory.check_token(data['token'])==False):
            self.transport.loseConnection()
        commands=data.items()
        commands.reverse()
        self.factory.write_socket(json.dumps(commands[1:]))
