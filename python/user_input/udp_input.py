#!/usr/bin/env python3

import socket

class udp_input:
    def __init__(self, listen_ip, listen_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((listen_ip, listen_port))

    def get_user_input(self, timeout_sec):
        self.sock.settimeout(timeout_sec)
        try:
            data = self.sock.recv(1)
            print("ktktktktk   " + str(data))
            return data
        except:
            return False
