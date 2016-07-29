'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys, random, string, time
from luzi82.pkmgo import common as vcommon
import memcache

rand_key_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
def gen_key():
    return ("".join(random.choice(rand_key_charset)for _ in range(50)))+str(int(time.time()*1000))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        vcommon.perr ('{0} memcache_addr sec'.format(sys.argv[0]))
        exit()
    
    arg_memcache_addr = sys.argv[1]
    arg_sec = int(sys.argv[2])
    
    mc = memcache.Client([arg_memcache_addr])
    
    for line in sys.stdin:
        l = line.rstrip('\n')
        key = gen_key()
        mc.set(key,l,time=arg_sec)
        vcommon.pout(key)
