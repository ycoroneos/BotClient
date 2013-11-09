import socket
import sys

HOST=sys.argv[1]
PORT=sys.argv[2]

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((HOST, int(PORT)))
s.settimeout(1.00);
cmd='nothing yet!\n'
while (cmd!='quit'):
    s.sendall(cmd+'\n');
    try:
        print (s.recv(1024)+'\n')
    except:
        pass
    cmd=raw_input();
s.close()
