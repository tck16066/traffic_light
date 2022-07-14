#!/usr/bin/env python3

# Dummy class can be used for testing

class light_interface_dummy:
    def __init__(self):
        light_hw = {'red': None,
                    'yellow': None,
                    'green': None,
                   }

    def light_on(self, config):
        print("turning on %s" % config['name'])

    def light_off(self, config):
        print("turning off %s" % config['name'])
