BotClient
=========

Data visualizer and communicator for MASLAB

Initial Framework Idea:
There are 2 basic types of servers. There is the robot comms server
which directly facilitates communication with MASLAB bots. It listens on
an arbitrary socket. No more than 2 bots may be connected (enforced
through a lax check that can be alleviated in the future). Each bot
connection spawns a new 'protocol' which is actually a process.
