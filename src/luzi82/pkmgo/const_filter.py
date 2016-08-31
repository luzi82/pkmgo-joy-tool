'''
Created on Aug 28, 2016

@author: luzi82
'''

import sys
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 2:
        vcommon.perr ('{0} const'.format(sys.argv[0]))
        exit()
    
    arg_const = sys.argv[1]
    
    for line in sys.stdin:
        vcommon.pout(arg_const)
