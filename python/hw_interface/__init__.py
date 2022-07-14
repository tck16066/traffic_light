#!/usr/bin/env python3

# This will merge the light and audio interfaces.

class hw_interface:
    def __init__(self, light_interface):

       self.light_interface = light_interface

       self.red_config = {
           'name' : 'red',
           'audio_gen': None
       }
        
        
       self.yellow_config = {
           'name' : 'yellow',
           'audio_gen': None
       }
        
        
       self.green_config = {
           'name' : 'green',
           'audio_gen': None
       }
        
        
       self.light_configs = {
           'r' : self.red_config,
           'y' : self.yellow_config,
           'g' : self.green_config,
       }

    def hw_light_on(self, config_abbrev):
        self.light_interface.light_on(self.light_configs[config_abbrev])
        # TODO audio here too
    
    
    def hw_light_off(self, config_abbrev):
        self.light_interface.light_off(self.light_configs[config_abbrev])
        # TODO audio here too

    def hw_all_off(self):
        for y in list(self.light_configs.keys()):
            self.hw_light_off(y)
            # TODO audio

__all__ = ['hw_interface']

