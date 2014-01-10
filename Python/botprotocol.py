from twisted.internet import protocol, reactor
from twisted.protocols import basic
import json, handler, re

#this needs to be improved so that the token must not be checked every command. Probably the best improvement is to save the session
#in the factory by checking the token once

done_regex=re.compile('done')
ping_regex=re.compile('ping')

class BotProtocol(basic.LineReceiver):
    MAX_LENGTH=90000
    def connectionMade(self):
        self.factory.addConnection(self)
        self.user=False
        self.tmpline=''
        self.transport.write("weee you connected\r\n")

    def connectionLost(self, reason):
        self.factory.removeConnection(self)

    def dataReceived(self, line):
        result=ping_regex.match(line)
        if (result!=None):
            self.transport.write("connected")
            return
        line=line[:-1]
        self.tmpline+=line
        print line[-4:]
        result=done_regex.match(line[-4:])
        if (result!=None):
            print 'ok parsing line\n'
            self.tmpline=self.tmpline[:-(len(result.group(0)))]
            self.parseline()
            self.tmpline=''
        else:
            return
    def parseline(self):
        print 'input: ' + str(self.tmpline) + '\n'
        try:
            data=json.loads(self.tmpline)
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
            del data['token']
            commands=data.items()
            dispatch=[]
            for i in commands:
                dispatch+=[self.user]+[x for x in i]
            self.factory.broadcast(dispatch)
            handler.addtoqueue(dispatch)
        else:
            print 'valid user\n'
            del data['token']
            commands=data.items()
            dispatch=[]
            for i in commands:
                dispatch+=[self.user]+[x for x in i]
            print 'whats going in the queue: ' + str(dispatch)+'\n'
            handler.addtoqueue(dispatch)
