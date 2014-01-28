from twisted.internet import protocol, reactor
from twisted.protocols import basic
import json, handler, re

#this needs to be improved so that the token must not be checked every command. Probably the best improvement is to save the session
#in the factory by checking the token once

done_regex=re.compile('done')
ping_regex=re.compile('ping\n')
game_regex=re.compile('game\n')
game_running=False


class BotProtocol(basic.LineReceiver):
    MAX_LENGTH=90000
    def connectionMade(self):
        self.factory.addConnection(self)
        self.user=False
        self.tmpline=''
        self.transport.write("connected\r\n")

    def connectionLost(self, reason):
        self.factory.removeConnection(self)

    def dataReceived(self, line):
        #print line+'\n'
        result=None
        result=ping_regex.match(line)
        if (result!=None):
            self.transport.write("pong\r\n")
            return
        result=game_regex.match(line)
        if (result!=None):
            self.transport.write(str(game_running)+'\r\n')
            return
        #line=line[:-1]
        self.tmpline+=line
        print line[-5:]
        result=done_regex.match(line[-5:])
        if (result!=None):
            print 'ok parsing line\n'
            self.tmpline=self.tmpline[:-(len('done'))]
            self.tmpline=self.tmpline[:-1]
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
            if ('MSG' in data):
                commands=data.items()
                dispatch=[]
                for i in commands:
                    dispatch+=[self.user]+[x for x in i]
                handler.addtoqueue(dispatch)
            else:
                self.factory.broadcast(json.dumps(data))
                try:
                    if (data['GAME']=='start'):
                        game_running=True
                    elif (data['GAME']=='stop'):
                        game_running=False
                except:
                    pass
        else:
            print 'valid user\n'
            del data['token']
            commands=data.items()
            dispatch=[]
            for i in commands:
                dispatch+=[self.user]+[x for x in i]
            print 'whats going in the queue: ' + str(dispatch)+'\n'
            handler.addtoqueue(dispatch)
