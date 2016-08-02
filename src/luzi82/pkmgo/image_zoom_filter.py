'''
Created on Jul 30, 2016

@author: luzi82
'''

import sys
import numpy
import base64
import scipy.ndimage
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 4:
        vcommon.perr('{0} ori_width ori_height factor'.format(sys.argv[0]))
        exit()
    arg_ori_width   = int(sys.argv[1])
    arg_ori_height  = int(sys.argv[2])
    arg_factor  = int(sys.argv[3])
    
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
        out_bgr_list2 = scipy.ndimage.zoom(in_bgr_list2, [arg_factor,arg_factor,1], order=3)
        out_bgr_list2 = out_bgr_list2.astype(int)
        out_bgr_list2 = numpy.minimum(out_bgr_list2,255)
        out_bgr_list2 = numpy.maximum(out_bgr_list2,0)
        out_data = bytes(list(numpy.reshape(out_bgr_list2,[-1])))
#         vcommon.perr('DTBHZGSF '+str(out_bgr_list2.shape))
#         vcommon.perr('IDMUCAXU len(out_bgr_list2)={0}, len(out_bgr_list2[0])={1}, len(out_bgr_list2[0][0])={2}, len(out_data)={3}'.format(
#             len(out_bgr_list2),
#             len(out_bgr_list2[0]),
#             len(out_bgr_list2[0][0]),
#             len(out_data),
#         ))
        out_data_b64 = base64.b64encode(out_data)
        vcommon.pout(out_data_b64.decode('utf-8'))
