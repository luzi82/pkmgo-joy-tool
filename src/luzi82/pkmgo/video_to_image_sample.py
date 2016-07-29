'''
Created on Jul 23, 2016

Get image sample from video for train

@author: luzi82
'''
import sys, os, time
import numpy
import cv2
from luzi82.pkmgo import common as vcommon

# width height sec output_path
if __name__ == '__main__':
    if len(sys.argv) != 5:
        vcommon.perr ('{0} width height sec output_path'.format(sys.argv[0]))
        exit()
    arg_width = int(sys.argv[1])
    arg_height = int(sys.argv[2])
    arg_image_sec = int(sys.argv[3])
    arg_output_path = sys.argv[4]
    
    if not os.path.isdir(arg_output_path):
        os.makedirs(arg_output_path)
    if not os.path.isdir(arg_output_path):
        vcommon.perr('NTGFQWHQ Cannot create directory')
        exit()
    
    byte_count = arg_width * arg_height * 3

    last_image_timestamp = 0
    
    while True:
        byte_list = sys.stdin.buffer.read(byte_count)
        if byte_list == None:
            vcommon.perr('CXSVTELX byte_list == None')
            break
        if len(byte_list) != byte_count:
            vcommon.perr('GTPAZPAY len(byte_list) != byte_count')
            break
        now = time.time()
        if now - last_image_timestamp < arg_image_sec:
            continue
        bgr_list2 = numpy.reshape(list(byte_list),[arg_height,arg_width,3])
        cv2.imwrite('{0}/{1}.png'.format(arg_output_path,str(int(now))),bgr_list2)
        last_image_timestamp = now
        #image_done_count += 1
