#!/usr/bin/env python3

from .light_interface_dummy import *

__all__ = ['light_interface_dummy']


f = open('/proc/cpuinfo', 'r')
dat = f.read()
if 'BCM2708' in dat or 'BCM2709' in dat:
    print("found BCM2708 or BCM2709")
    from .light_interface_pi import *
    __all__.append('light_interface_pi')
    print(__all__)
f.close()
