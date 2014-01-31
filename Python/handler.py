from multiprocessing import Process, Queue, Value

maxqsize=5
commandq=Queue()    #contains items in format (user, field, data)

admincommand=None

def addtoqueue(dispatch):
    if (commandq.qsize()<=maxqsize):
        commandq.put(dispatch)
    else:
        print 'queue is too large\n'
