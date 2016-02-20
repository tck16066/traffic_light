#!/usr/bin/python
import sys
from select import select

class stdin_input:
    def get_user_input(self, timeout):
        """
        Returns None, or keys read.
        """
        try:
            rlist, _, _ = select([sys.stdin], [], [], timeout)
        except:
           rlist = False
           pass

        if rlist:
            s = sys.stdin.readline()
            return s.strip()
        else:
            return None
