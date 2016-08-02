'''
Created on Jul 30, 2016

@author: luzi82
'''

import sys
import numpy
import base64
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 4:
        vcommon.perr('{0} byte_count min max'.format(sys.argv[0]))
        exit()
    arg_byte_count = int(sys.argv[1])
    arg_min = int(sys.argv[2])
    arg_max = int(sys.argv[3])
    
    min_p = arg_min / 100
    max_p = arg_max / 100
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('TWCUXJBR byte_list == None')
            break
        in_data_b64 = line.rstrip('\n')
        in_data = base64.b64decode(in_data_b64)
        if len(in_data) != arg_byte_count:
            vcommon.perr('JMVBUHTM len(byte_list) != byte_count')
            continue
        tmp_data_np = numpy.reshape(list(in_data),[arg_byte_count])
        data_min = numpy.amin(tmp_data_np)
        data_max = numpy.amax(tmp_data_np)
        tmp_data_np = tmp_data_np - data_min
        tmp_data_np = tmp_data_np / (data_max - data_min)
        tmp_data_np = tmp_data_np - min_p
        tmp_data_np = tmp_data_np / (max_p-min_p)
        tmp_data_np = tmp_data_np * 255
        tmp_data_np = tmp_data_np.astype(int)
        tmp_data_np = numpy.minimum(tmp_data_np,255)
        tmp_data_np = numpy.maximum(tmp_data_np,0)
        out_data = bytes(list(tmp_data_np))
#         vcommon.perr('IDMUCAXU len(out_bgr_list2)={0}, len(out_bgr_list2[0])={1}, len(out_bgr_list2[0][0])={2}, len(out_data)={3}'.format(
#             len(out_bgr_list2),
#             len(out_bgr_list2[0]),
#             len(out_bgr_list2[0][0]),
#             len(out_data),
#         ))
        out_data_b64 = base64.b64encode(out_data)
        vcommon.pout(out_data_b64.decode('utf-8'))
