'''
Created on Jul 30, 2016

@author: luzi82
'''

import sys, os, time
import numpy
import cv2
import base64
from luzi82.pkmgo import common as vcommon
import pytesseract
from PIL import Image

if __name__ == '__main__':
    if len(sys.argv) != 3:
        vcommon.perr('{0} width height'.format(sys.argv[0]))
        exit()

    arg_width = int(sys.argv[1])
    arg_height = int(sys.argv[2])

    byte_count = arg_width * arg_height * 3
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('ZVYXGFQN line == None')
            break
        
        data_b64 = line.rstrip('\n')
        data = base64.b64decode(data_b64)
        if len(data) != byte_count:
            vcommon.perr('PILJLIOU len(data) != byte_count, len(data)={0}, byte_count={1}'.format(len(data),byte_count))
            continue

        bgr_list2 = numpy.reshape(list(data),[arg_height,arg_width,3])
        
        txt = pytesseract.image_to_string(Image.fromarray(numpy.uint8(bgr_list2)),config="-psm 7")
        vcommon.pout(txt)
