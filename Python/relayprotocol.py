from twisted.internet import protocol, reactor
from multiprocessing import Process, Queue
from twisted.protocols import basic
import json, re

user_regex=re.compile('set user ')

class BotRelayProtocol(basic.LineReceiver):
    def connectionMade(self):
        if (self.factory.isconnected==False):
            self.transport.write("Someone's already connected idiot...\r\n")
            self.transport.loseConnection()
        else:
            self.factory.connect()

    def connectionLost(self, reason):
        self.factory.disconnect()

    def lineReceived(self, line):
        if (line=="n"):
            command=botclient.commandq.get()
            if (command[0]!=self.factory.gettargetuser()):
                botclient.commandq.put(command)
            else:
                self.transport.write(json.dumps(command))
        else:
            result=user_regex.match(line)
            user=line[len(result.group(0)):]
            self.factory.settargetuser(user)
