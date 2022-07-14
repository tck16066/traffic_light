#!/usr/bin/env python3

import RPi.GPIO as GPIO

class light_interface_pi:
    def __init__(self):
        self.light_hw = {'red': 2,
                        'yellow': 3,
                        'green': 4,
                       }

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for x in list(self.light_hw.values()):
            GPIO.setup(x, GPIO.OUT)
            GPIO.output(x, 0)

    def light_on(self, config):
        GPIO.output(self.light_hw[config['name']], 1)

    def light_off(self, config):
        GPIO.output(self.light_hw[config['name']], 0)

