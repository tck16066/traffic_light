from collections import namedtuple
from random import choice, random

sequence_entry = namedtuple('sequence_entry', 'color_abbrev')

class sequence_interface:
    """
    This defines a few functions used for generating sequence entries (for
    instance, used in a simon game).
    """

    def __init__(self):
        self.options = [sequence_entry('r'),
                        sequence_entry('y'),
                        sequence_entry('g')]

    def generate_n_entries(self, n):
        """
        Used for testing
        """
        seq = []
        for x in range (0, n):
            seq.append(self.sequence_generate_entry())
        return seq

    @staticmethod
    def sequence_entry_eq(entry1, entry2):
        return entry1.color_abbrev == entry2.color_abbrev
    
    def sequence_generate_entry(self):
        """
        Creates an entry in a sequence, random choice.
        """
        
        return choice(self.options)

