#!/usr/bin/env python3

from itertools import cycle
import threading

class traffic_pattern_game:
    def __init__(self, hw_interface):
        #
        # This is what we use to interact with the hardware
        #
        self.hw_interface = hw_interface

        #
        # Red light duration
        #
        self.red_light_msecs = 30000 * 0.001

        #
        # Yellow light duration
        #
        self.yellow_light_msecs = 4000 * 0.001

        #
        # Green light duration
        #
        self.green_light_msecs = 60000 * 0.001

        #
        # Is the game running?
        #
        self.game_running = False

        #
        # Light lights up in this order
        #
        self.light_rules = cycle([('r', self.red_light_msecs),
                                  ('g', self.green_light_msecs),
                                  ('y', self.yellow_light_msecs)])

        #
        # Timer used for lighting the lights
        #
        self.light_timer = None

    def next_light(self):
        """
        Set timer for next light and light the light.
        """
        light = next(self.light_rules)
        self.hw_interface.hw_all_off()
        self.hw_interface.hw_light_on(light[0])
        self.light_timer = threading.Timer(light[1], self.next_light)
        self.light_timer.start()

    def start_game(self):
        """
        Fire off the start of the traffic pattern game. Lights light up.
        """
        self.hw_interface.hw_all_off()
        self.next_light()
        self.game_running = True

    def handle_input(self, input_data):
        """
        Filter all non-light-button input, stop game otherwise.
        """
        vals = ['r', 'y', 'g']
        if input_data not in vals:
            return

        if self.light_timer is not None:
            self.light_timer.cancel()
        self.game_running = False
