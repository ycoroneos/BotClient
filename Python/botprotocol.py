from twisted.internet import protocol, reactor
from twisted.protocols import basic
import json, handler, re, copy

#this needs to be improved so that the token must not be checked every command. Probably the best improvement is to save the session
#in the factory by checking the token once

done_regex=re.compile('done')
ping_regex=re.compile('ping\n')
game_regex=re.compile('game\n')


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
            self.transport.write(self.factory.game_running+'\r\n')
            print "received game ping request: " + self.factory.game_running + '\n'
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
                if ('GAME' in data):
                    if (data['GAME']=="start"):
                        print "STARTING GAME\n"
                        self.factory.game_running='{"GAME":"start"}'
                    elif (data['GAME']=="stop"):
                        print "STOPPING GAME\n"
                        self.factory.game_running='{"GAME":"stop"}'
                if ('left_team' in data):
                    self.factory.left_team=copy.copy(str(data['left_team']))
                    del data['left_team']
                if ('right_team' in data):
                    self.factory.right_team=copy.copy(str(data['right_team']))
                    del data['right_team']
                if ('left_map' in data):
                    print 'setting left map\n'
                    self.factory.left_map=copy.copy(str(data['left_map']))
                    del data['left_map']
                if ('right_map' in data):
                    print 'setting right map\n'
                    self.factory.right_map=copy.copy(str(data['right_map']))
                    del data['right_map']
                if (len(data)>0):
                    self.factory.broadcast(json.dumps(data)+'\n')
        else:
            print 'valid user\n'
            del data['token']
            if ('MAP' in data):
                if (self.user==self.factory.right_team):
                    print 'sending ' + str(self.user) + ' the map: ' + self.factory.right_map + '\n'
                    self.transport.write('{"MAP":"'+self.factory.right_map+'"}\n')
                else:
                    print 'sending ' + str(self.user) + ' the map: ' + self.factory.left_map + '\n'
                    self.transport.write('{"MAP":"'+self.factory.left_map+'"}\n')
                del data['MAP']
            commands=data.items()
            dispatch=[]
            for i in commands:
                dispatch+=[self.user]+[x for x in i]
            print 'whats going in the queue: ' + str(dispatch)+'\n'
            handler.addtoqueue(dispatch)
