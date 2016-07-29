'''
Created on Jul 24, 2016

@author: luzi82
'''
import sys
import time
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 2:
        vcommon.perr ('{0} ms'.format(sys.argv[0]))
        exit()
    
    arg_sec = int(sys.argv[1])
    
    last_timestamp = 0
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('MJDXATAO byte_list == None')
            break
        now = time.time()*1000
        if now - last_timestamp < arg_sec:
            continue
        l = line.rstrip('\n')
        vcommon.pout(l)
#         vcommon.perr('MICDBJNS '+str(len(l)),file=sys.stderr)
        last_timestamp = now
