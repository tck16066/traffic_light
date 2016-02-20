#/usr/bin/python

import imp
import os
import sys
import argparse
import signal

from hw_interface import *
from light_interface import *
from simon import *
from sequence import *

import sequence
import traffic_pattern
import user_input

def sig_handler(signum, frame):
    print "Exiting game..."
    os._exit(0)

signal.signal(signal.SIGINT, sig_handler)

parser = argparse.ArgumentParser(description='Options for traffic light program')
parser.add_argument('--udp-port', nargs=1, type=int,
                   help='UDP port to listen on for input. If not specific, use keyboard.')


args = parser.parse_args()


if args.udp_port == None:
    x = user_input.stdin_input()
else:
    x = user_input.udp_input("", args.udp_port[0])

seq_iface = sequence_interface()

try:
    print "Using light_interface_pi"
    li = light_interface_pi()
except:
    print "Couldn't find light_interface_pi, using light_interface_dummy"
    li = light_interface_dummy()

hw = hw_interface(li)

s = simon(hw, seq_iface)
t = traffic_pattern.traffic_pattern_game(hw)

games = [t, s]


while True:
    for game in games:
        game.start_game()
        while game.game_running:
            inp = x.get_user_input(0.01)
            if inp:
                if inp == 'q':
                    inp = 'r'
                if inp == 'w':
                    inp = 'y'
                if inp == 'd':
                    inp = 'g'
                game.handle_input(inp)
