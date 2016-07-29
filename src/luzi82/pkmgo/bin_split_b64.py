'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys
import base64
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 2:
        vcommon.perr ('{0} byte_count'.format(sys.argv[0]))
        exit()
    
    arg_byte_count = int(sys.argv[1])
    
    while True:
        byte_list = sys.stdin.buffer.read(arg_byte_count)
        if byte_list == None:
            vcommon.perr('WPQITOAO byte_list == None')
            break
        if len(byte_list) != arg_byte_count:
            vcommon.perr('YMPVBAVQ len(byte_list) != arg_byte_count')
            break
        byte_list_b64 = base64.b64encode(byte_list)
        vcommon.pout(byte_list_b64.decode('utf-8'))
#         vcommon.perr('RZGCZYYC '+str(len(byte_list_b64)))
