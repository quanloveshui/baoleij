#!/usr/bin/env python

import sys,os




if __name__ == "__main__":

    from  backend import main
    interactive_obj = main.ArgvHandler(sys.argv)
    interactive_obj.call()
