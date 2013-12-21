from twisted.internet import protocol, reactor
from twisted.protocols import basic
import json, handler

#this needs to be improved so that the token must not be checked every command. Probably the bets improvement is to save the session
#in the factory by checking the token once

class BotProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.factory.addConnection()

    def connectionLost(self, reason):
        self.factory.removeConnection()

    def dataReceived(self, line):
        print line
        #line=line[:-2]
        try:
            data=json.loads(line[:-1])
        except:
            print 'failed decoding line\n'
            return
        print str(data) + '\n'
        user=self.factory.check_token(data['token'])
        if (user==False):
            self.transport.loseConnection()
        print 'valid user\n'
        commands=data.items()
        commands.reverse()
        commands=commands[1:]
        dispatch=[]
        for i in commands:
            dispatch+=[user]+[x for x in i]
        print str(dispatch)+'\n'
        handler.commandq.put(dispatch)
