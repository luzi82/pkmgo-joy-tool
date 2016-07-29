'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys

def pout(message):
    pp(message,sys.stdout)

def perr(message):
    pp(message,sys.stderr)

def pp(message,file):
    print(message,file=file)
    file.flush()
