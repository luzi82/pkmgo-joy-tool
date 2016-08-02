'''
Created on Jul 30, 2016

@author: luzi82
'''
import sys
import numpy
import base64
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr ('{0}'.format(sys.argv[0]))
        exit()
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('HKWISBHJ byte_list == None')
            break
        in_data_b64 = line.rstrip('\n')
        in_data = base64.b64decode(in_data_b64)
        sys.stdout.buffer.write(in_data)
        sys.stdout.flush()
