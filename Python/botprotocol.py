from twisted.internet import protocol, reactor
from twisted.protocols import basic
import json, handler

#this needs to be improved so that the token must not be checked every command. Probably the best improvement is to save the session
#in the factory by checking the token once

class BotProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.factory.addConnection(self)
        self.user=False

    def connectionLost(self, reason):
        self.factory.removeConnection(self)

    def dataReceived(self, line):
        print 'input: ' + str(line) + '\n'
        #line=line[:-2]
        try:
            data=json.loads(line[:-1])
        except:
            print 'failed decoding line\n'
            return
        print 'decoded json: ' + str(data) + '\n'
        self.user=self.factory.check_token(data['token'])
        if (self.user==False):
            print 'invalid user\n'
            return
        elif (self.user=='admin'):
            print 'admin is here Oo\n'
            self.factory.broadcast('imanadmin\n')
        else:
            print 'valid user\n'
            del data['token']
            commands=data.items()
            #commands=commands[1:]
            dispatch=[]
            for i in commands:
                dispatch+=[self.user]+[x for x in i]
            print 'whats going in the queue: ' + str(dispatch)+'\n'
            handler.commandq.put(dispatch)
