from twisted.internet import protocol, reactor
from multiprocessing import Process, Queue
from twisted.protocols import basic
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
import json, re, handler
from multiprocessing.sharedctypes import Value, Array

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
            #print 'ok, fetching the next command from ' + self.targetuser +'\n'
            if (handler.admincommand!=None):
                self.sendMessage(json.dumps(handler.admincommand))
            qsize=handler.commandq.qsize()
            for i in range(0,qsize):
                command=handler.commandq.get()
                if (len(command)<1):
                    return
                if (command[0]==self.targetuser):
                    self.sendMessage(json.dumps(command))
                    return
                else:
                    handler.commandq.put(command)
            #print 'its nothing\n'
            self.sendMessage('none')
        else:
            result=user_regex.match(line)
            if (result!=None):
                user=line[len(result.group(0)):]
                print 'setting target user to: ' + user + '\n'
                self.targetuser=user
