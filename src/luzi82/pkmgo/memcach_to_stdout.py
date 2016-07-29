'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys
from luzi82.pkmgo import common as vcommon
import memcache

if __name__ == '__main__':
    if len(sys.argv) != 2:
        vcommon.perr ('{0} memcache_addr'.format(sys.argv[0]))
        exit()
    
    arg_memcache_addr = sys.argv[1]
    
    mc = memcache.Client([arg_memcache_addr])
    
    for line in sys.stdin:
        key = line.rstrip('\n')
        l = mc.get(key)
        vcommon.pout(l)
