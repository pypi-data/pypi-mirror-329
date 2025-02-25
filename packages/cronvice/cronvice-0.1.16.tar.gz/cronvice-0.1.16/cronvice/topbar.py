#!/usr/bin/env python3

# from {proj}.version import __version__
import time
import datetime as dt
import os
from fire import Fire
from pytermgui import print_to, report_cursor, save_cursor, restore_cursor
from cronvice import config
# import threading  # for key input

from console import fg, bg, fx
import socket
import hashlib
# theight= terminal.height
# twidth= terminal.width

global_mode = " "

def get_hostname():
    return socket.gethostname()

def get_deterministic_number():
    hostname = socket.gethostname()
    hash_value = hashlib.sha256(hostname.encode()).hexdigest()
    return int(hash_value, 16) % 10


class Topbar:
    """
    allows to define top bar(s) and keep printing them
    """

    host_colors =  [ bg.slateblue,   bg.brown, bg.purple,   bg.darkcyan, bg.cadetblue, bg.darkslateblue, bg.darkgreen,  bg.sienna,  bg.indianred, bg.seagreen]
    def __init__(self, pos=1, bgcolor="auto"):
        self.pos = pos
        self.positions = {}
        self.t2 = None
        if bgcolor is None:
            self.BCOL = bg.blue
        elif bgcolor == "auto":
            i = get_deterministic_number()
            self.BCOL = self.host_colors[i]
        else:
            self.BCOL = bgcolor

    @classmethod
    def get_colors(cls):
        return cls.host_colors

        # self.t = threading.currentThread()

        # try:
        #     pass
        #     # print("report_cursor to appear")
        #     # print( "i... topbar: pos/cursor",pos  )
        #     report_cursor()
        #     # print("report done")
        # except:
        #     print("X... problem with report_cursor")
        # # print("i... topbar bar started")

    def add(self, two=2, bgcolor=bg.blue):
        """
        create second bar
        """
        if two == 2:
            self.t2 = Topbar(two, bgcolor=bgcolor)
        else:
            print("X... nobody wanted more than two......  NOT OK")
        return self.t2

    def print_to(self, tup, s):
        """
        insert into the bar
        """
        if isinstance(tup, tuple):
            x = tup[0]
            print("X.......... TUPLE in the TOPBAR  IS SUPRESSED")
        elif isinstance(tup,int):
            x = tup
            # y = 1
        else:
            print(
                "X... only tuple or int in the TOPBAR  position"
            )
        self.positions[x] = s

    def place(self):
        """
        Place he BAR on screen
        """
        # curs = (-1, -1)
        #twidth = os.get_terminal_size().columns
        twidth = config.get_terminal_columns() # os.get_terminal_size().columns

        if self.pos == 1:
            save_cursor()
        print_to((1, self.pos), f"{self.BCOL}" + " " * twidth + bg.default)
        print_to((1, self.pos + 1), " " * twidth)

        # self.positions[ twidth] = f"{fx.default}{fg.default}{bg.default}"

        for k in self.positions.keys():
            print_to(
                (k, self.pos),
                f"{self.BCOL}{self.positions[k]}{bg.default}{fx.default}\
{fg.default}",
            )

        if self.t2 is not None:
            self.t2.place()

        if self.pos == 1:
            restore_cursor()
            print("", end="\r")  # this make GOOD thing in printing


def main():
    """
    print an example top bar
    """
    t = Topbar(1)

    # BOTH
    # bg.cadetblue  bg.steelblue bg.darkgreen, bg.olive
    # bg.steelblue, is too close
    print("\n\n\n\n\n\n")
    for c in [ bg.navy, bg.steelblue]:
        print(fg.white, c, "        SEE an example of a top bar  -  ",fg.black, "kill with  Ctrl-c     ", bg. default)


    print(fg.white, "with  WHITE LETTERS   10 colors !") # bg.olive,

    for c in Topbar.get_colors():
        print(fg.white, c, "        SEE an example of a top bar  -  ",fg.black, "kill with  Ctrl-c     ", bg. default)


    # print(fg.white, "with  BLACK LETTERS")
    # for c in [  bg.orange, bg.khaki, bg.burlywood, bg.aquamarine, bg.sandybrown, bg.tomato, bg.salmon, bg.lightcoral,]:
    #     print(fg.black, c, "        SEE an example of a top bar  -  ",fg.white, "kill with  Ctrl-c     ", bg. default)

    for i in range(100):
        #
        # DO whatever stuff and PLACE PRINTTO SLEEP
        #
        t.place()
        t.print_to(11, f"{fg.white} {str(dt.datetime.now())[:-4]} {fg.default}")
        time.sleep(0.1)


if __name__ == "__main__":
    Fire(main)
