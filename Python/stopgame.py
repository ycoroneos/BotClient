#!/usr/bin/python2.7
import socket, sys, time, base64, json

# startgame.py host port left_team right_team left_map right_map

HOST=sys.argv[1]
PORT=sys.argv[2]
stop_game_cmd='{"token":"EViL","GAME":"stop"}done\n'

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((HOST, int(PORT)))
s.sendall(stop_game_cmd)
s.close()
