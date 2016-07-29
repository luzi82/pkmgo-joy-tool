'''
Created on Jul 24, 2016

@author: luzi82
'''
import sys, random, string, time
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 2:
        vcommon.perr ('{0} ms'.format(sys.argv[0]))
        exit()
        
    arg_ms = int(sys.argv[1])
        
    charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
    
    x = 0
    
    while True:
        vcommon.pout("".join(random.choice(charset)for x in range(64)))
        time.sleep(arg_ms/1000.)
