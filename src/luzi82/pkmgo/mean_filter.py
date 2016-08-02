'''
Created on Jul 30, 2016

@author: luzi82
'''

import sys
import numpy
import base64
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 3:
        vcommon.perr ('{0} byte_count frame_count'.format(sys.argv[0]))
        exit()
    
    arg_byte_count = int(sys.argv[1])
    arg_frame_count = int(sys.argv[2])
    
    bgr_sum_list = None
    frame_done = 0
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('HKWISBHJ byte_list == None')
            break
        in_data_b64 = line.rstrip('\n')
        in_data = base64.b64decode(in_data_b64)
        if len(in_data) != arg_byte_count:
            vcommon.perr('SBYEIHYG len(byte_list) != byte_count')
            continue
        in_bgr_list2 = numpy.reshape(list(in_data),[arg_byte_count])
        if bgr_sum_list is None:
            bgr_sum_list = numpy.zeros([arg_byte_count])
        bgr_sum_list = numpy.sum([bgr_sum_list,in_bgr_list2],axis=0)
        frame_done = frame_done+1
        if frame_done >= arg_frame_count:
            bgr_sum_list = bgr_sum_list / frame_done
            bgr_sum_list = bgr_sum_list.astype(int)
            out_data = bytes(list(bgr_sum_list))
            out_data_b64 = base64.b64encode(out_data)
            vcommon.pout(out_data_b64.decode('utf-8'))
            bgr_sum_list = None
            frame_done = 0
    
    pass