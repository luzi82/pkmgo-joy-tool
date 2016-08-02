'''
Created on Jul 24, 2016

@author: luzi82
'''
import sys
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 2:
        vcommon.perr ('{0} skip'.format(sys.argv[0]))
        exit()
    
    arg_skip = int(sys.argv[1])
    
    done = 0
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('MJDXATAO byte_list == None')
            break
        done += 1
        if done < arg_skip:
            continue
        done = 0
        l = line.rstrip('\n')
        vcommon.pout(l)
