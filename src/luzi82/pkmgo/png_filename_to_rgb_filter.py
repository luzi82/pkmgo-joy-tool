'''
Created on Jul 29, 2016

@author: luzi82
'''

import sys
import cv2, numpy
import base64
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr('{0}'.format(sys.argv[0]))
        exit()
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('URATRYYK byte_list == None')
            break
        filename = line.rstrip('\n')
        bgr_list2 = cv2.imread(filename)
        byte_list = numpy.reshape(bgr_list2,[-1])
        byte_list_b64 = base64.b64encode(byte_list)
        vcommon.pout(byte_list_b64.decode('utf-8'))
