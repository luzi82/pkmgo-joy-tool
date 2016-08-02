'''
Created on Jul 30, 2016

@author: luzi82
'''

import sys
import numpy
import base64
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 7:
        vcommon.perr('{0} ori_width ori_height chop_left chop_top chop_width chop_height'.format(sys.argv[0]))
        exit()
    arg_ori_width   = int(sys.argv[1])
    arg_ori_height  = int(sys.argv[2])
    arg_chop_left   = int(sys.argv[3])
    arg_chop_top    = int(sys.argv[4])
    arg_chop_width  = int(sys.argv[5])
    arg_chop_height = int(sys.argv[6])
    
    byte_count = arg_ori_width * arg_ori_height * 3

    for line in sys.stdin:
        if line == None:
            vcommon.perr('HKWISBHJ byte_list == None')
            break
        in_data_b64 = line.rstrip('\n')
        in_data = base64.b64decode(in_data_b64)
        if len(in_data) != byte_count:
            vcommon.perr('SBYEIHYG len(byte_list) != byte_count')
            continue
        in_bgr_list2 = numpy.reshape(list(in_data),[arg_ori_height,arg_ori_width,3])
        out_bgr_list2 = in_bgr_list2[
            arg_chop_top :arg_chop_top +arg_chop_height,
            arg_chop_left:arg_chop_left+arg_chop_width,
            :
        ]
        out_data = bytes(list(numpy.reshape(out_bgr_list2,[-1])))
#         vcommon.perr('IDMUCAXU len(out_bgr_list2)={0}, len(out_bgr_list2[0])={1}, len(out_bgr_list2[0][0])={2}, len(out_data)={3}'.format(
#             len(out_bgr_list2),
#             len(out_bgr_list2[0]),
#             len(out_bgr_list2[0][0]),
#             len(out_data),
#         ))
        out_data_b64 = base64.b64encode(out_data)
        vcommon.pout(out_data_b64.decode('utf-8'))
