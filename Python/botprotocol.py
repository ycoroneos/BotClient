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
        user=self.factory.check_token(data['token'])
        if (user==False):
            self.transport.loseConnection()
        commands=data.items()
        commands.reverse()
        commands=commands[1:]
        dispatch=[]
        for i in commands:
            dispatch+=[user]+[x for x in i]
        botclient.commandq.put(dispatch)
