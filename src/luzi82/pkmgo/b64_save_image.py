'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys, os, time
import numpy
import cv2
import base64
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 4:
        vcommon.perr('{0} width height output_path'.format(sys.argv[0]))
        exit()
    arg_width = int(sys.argv[1])
    arg_height = int(sys.argv[2])
    arg_output_path = sys.argv[3]

    if not os.path.isdir(arg_output_path):
        os.makedirs(arg_output_path)
    if not os.path.isdir(arg_output_path):
        vcommon.perr('LUNHVEVX Cannot create directory')
        exit()

    byte_count = arg_width * arg_height * 3

    for line in sys.stdin:
        if line == None:
            vcommon.perr('AHHENXNI byte_list == None')
            break
        byte_list_b64 = line.rstrip('\n')
        vcommon.pout(byte_list_b64)
#         vcommon.perr('RZQWGJBB '+str(len(byte_list_b64)))
        byte_list = base64.b64decode(byte_list_b64)
        if len(byte_list) != byte_count:
            vcommon.perr('NTCZLINX len(byte_list) != byte_count')
            continue
        now = int(time.time()*1000)
        bgr_list2 = numpy.reshape(list(byte_list),[arg_height,arg_width,3])
        filename = '{0}/{1}.png'.format(arg_output_path,str(int(now)))
        cv2.imwrite(filename,bgr_list2)
#         vcommon.perr(filename)
