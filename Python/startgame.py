#!/usr/bin/python2.7
import socket, sys, time, base64, json

# startgame.py host port left_team right_team left_map right_map

HOST=sys.argv[1]
PORT=sys.argv[2]
left_team=sys.argv[3]
right_team=sys.argv[4]
left_map=sys.argv[5]
right_map=sys.argv[6]
lmap=open(left_map, 'r').read()[:-1]
rmap=open(right_map, 'r').read()[:-1]
lteam_cmd='{"token":"EViL","left_team":"'+left_team+'"}done\n'
rteam_cmd='{"token":"EViL","right_team":"'+right_team+'"}done\n'
lmap_cmd='{"token":"EViL","left_map":"'+lmap+'"}done\n'
rmap_cmd='{"token":"EViL","right_map":"'+rmap+'"}done\n'
start_game_cmd='{"token":"EViL","GAME":"start"}done\n'
stop_game_cmd='{"token":"EViL","GAME":"stop"}done\n'

wait=0.05

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((HOST, int(PORT)))
s.sendall(lteam_cmd)
time.sleep(wait)
s.sendall(rteam_cmd)
time.sleep(wait)
s.sendall(lmap_cmd)
time.sleep(wait)
s.sendall(rmap_cmd)
time.sleep(wait)
s.sendall(start_game_cmd)
timestamp=time.time()
curtime=time.time()
while (curtime-timestamp<3*60):
    s.sendall('{"token":"EViL","MSG":["Time","'+str(curtime-timestamp)+'"]}done\n')
    time.sleep(wait)
    curtime=time.time()
s.sendall(stop_game_cmd)
s.sendall('{"token":"EViL","MSG":["Time","180"]}done\n')
s.close()
