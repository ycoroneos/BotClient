from multiprocessing import Process, Queue, Value

commandq=Queue()    #contains items in format (user, field, data)
