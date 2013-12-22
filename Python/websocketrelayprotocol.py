from twisted.internet import protocol, reactor
from multiprocessing import Process, Queue
from twisted.protocols import basic
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
import json, re, handler

user_regex=re.compile('set user ')

class BotRelayProtocol(WebSocketServerProtocol):
    def onOpen(self):
    	self.targetuser=None

    def connectionLost(self, reason):
        self.targetuser=None
        print 'someone lost connection...\n'

    def onMessage(self, line, binary):
        #user=self.factory.gettargetuser()
        if (line=="n" and self.targetuser!=None):
            #cycle through the queue until a command which matches our target user is found
            #this has the potential to infinitely loop so fix that later
            print 'ok, fetching the next command from ' + self.targetuser +'\n'
            qsize=handler.commandq.qsize()
            for i in range(0,qsize):
                command=handler.commandq.get()
                if (command[0]==self.targetuser):
                    self.sendMessage(json.dumps(command))
                    return
                else:
                    handler.commandq.put(command)
            print 'its nothing\n'
            self.sendMessage('none')
        else:
            result=user_regex.match(line)
            if (result!=None):
                user=line[len(result.group(0)):]
                print 'setting target user to: ' + user + '\n'
                self.targetuser=user
