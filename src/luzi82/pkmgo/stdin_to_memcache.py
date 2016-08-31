'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys
from luzi82.pkmgo import common as vcommon
import memcache

if __name__ == '__main__':
    if len(sys.argv) != 4:
        vcommon.perr ('{0} memcache_addr key sec'.format(sys.argv[0]))
        exit()
    
    arg_memcache_addr = sys.argv[1]
    arg_key = sys.argv[2]
    arg_sec = int(sys.argv[3])
    
    mc = memcache.Client([arg_memcache_addr])
    
    for line in sys.stdin:
        l = line.rstrip('\n')
        mc.set(arg_key,l,time=arg_sec)
        vcommon.pout(l)
