'''
Created on Jul 23, 2016

Transform screen shot to screen information

@author: luzi82
'''

import sys
import numpy
import base64
from luzi82.pkmgo import common as vcommon
from luzi82.pkmgo import frame_info_filter_data as mydata
import pytesseract
from PIL import Image
import json
import scipy.ndimage

def crop_grayscale_contrast_tesseract(bgr_list2,x,y,w,h,replace_dict,zoom=1):
    tmp_bgr_list2 = bgr_list2
#     tmp_bgr_list2 = numpy.array(tmp_bgr_list2)
    # crop
    tmp_bgr_list2 = tmp_bgr_list2[y:y+h,x:x+w,:]
    # grayscale
    tmp_bgr_list2 = numpy.average(tmp_bgr_list2, axis=2)
    tmp_bgr_list2 = numpy.repeat(tmp_bgr_list2, repeats=3, axis=1)
    tmp_bgr_list2 = numpy.reshape(tmp_bgr_list2, [h,w,3])
    tmp_bgr_list2 = tmp_bgr_list2.astype(int)
    # zoom
    if zoom != 1:
        tmp_bgr_list2 = scipy.ndimage.zoom(tmp_bgr_list2, [zoom,zoom,1], order=3)
    # contrast
    tmp_min = numpy.amin(tmp_bgr_list2)
    tmp_max = numpy.amax(tmp_bgr_list2)
    tmp_bgr_list2 = tmp_bgr_list2 - tmp_min
    tmp_bgr_list2 = tmp_bgr_list2 / max(1.,(tmp_max - tmp_min))
    tmp_bgr_list2 = tmp_bgr_list2 - vcommon.CONTRAST_MIN
    tmp_bgr_list2 = tmp_bgr_list2 / (vcommon.CONTRAST_MAX-vcommon.CONTRAST_MIN)
    tmp_bgr_list2 = tmp_bgr_list2 * 255
    tmp_bgr_list2 = tmp_bgr_list2.astype(int)
    tmp_bgr_list2 = numpy.minimum(tmp_bgr_list2,255)
    tmp_bgr_list2 = numpy.maximum(tmp_bgr_list2,0)
    # tesseract
    txt = pytesseract.image_to_string(Image.fromarray(numpy.uint8(tmp_bgr_list2)),config="-psm 7")
    for k, v in replace_dict.items():
        txt = txt.replace(k,v)
    return txt

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr ('{0}'.format(sys.argv[0]))
        exit()
        
    byte_count = vcommon.SCREEN_BYTE_COUNT

    for line in sys.stdin:
        if line == None:
            vcommon.perr('CFHRVFSI byte_list == None')
            break
        in_data_b64 = line.rstrip('\n')
        in_data = base64.b64decode(in_data_b64)
        if len(in_data) != byte_count:
            vcommon.perr('OQJPUNZY len(byte_list) != byte_count')
            continue
        in_bgr_list2 = numpy.reshape(list(in_data),[vcommon.SCREEN_HEIGHT,vcommon.SCREEN_WIDTH,3])
        cp_txt = crop_grayscale_contrast_tesseract(in_bgr_list2,
            vcommon.SCREEN_CP_X,vcommon.SCREEN_CP_Y,
            vcommon.SCREEN_CP_W,vcommon.SCREEN_CP_H,
            mydata.CP_TXT_REPLACE_DICT
        )
        hp_txt = crop_grayscale_contrast_tesseract(in_bgr_list2,
            vcommon.SCREEN_HP_X,vcommon.SCREEN_HP_Y,
            vcommon.SCREEN_HP_W,vcommon.SCREEN_HP_H,
            mydata.HP_TXT_REPLACE_DICT,4
        )
        powerup_stardust_txt = crop_grayscale_contrast_tesseract(in_bgr_list2,
            vcommon.SCREEN_POWERUP_STARDUST_X,vcommon.SCREEN_POWERUP_STARDUST_Y,
            vcommon.SCREEN_POWERUP_STARDUST_W,vcommon.SCREEN_POWERUP_STARDUST_H,
            mydata.POWERUP_STARDUST_TXT_REPLACE_DICT,4
        )
        powerup_candy_txt = crop_grayscale_contrast_tesseract(in_bgr_list2,
            vcommon.SCREEN_POWERUP_CANDY_X,vcommon.SCREEN_POWERUP_CANDY_Y,
            vcommon.SCREEN_POWERUP_CANDY_W,vcommon.SCREEN_POWERUP_CANDY_H,
            mydata.POWERUP_CANDY_TXT_REPLACE_DICT,4
        )
        candy_name_txt = crop_grayscale_contrast_tesseract(in_bgr_list2,
            vcommon.SCREEN_CANDY_NAME_X,vcommon.SCREEN_CANDY_NAME_Y,
            vcommon.SCREEN_CANDY_NAME_W,vcommon.SCREEN_CANDY_NAME_H,
            mydata.CANDY_NAME_TXT_REPLACE_DICT,4
        )
        ret = json.dumps({
            'cp':cp_txt,
            'hp':hp_txt,
            'powerup_stardust':powerup_stardust_txt,
            'powerup_candy':powerup_candy_txt,
            'candy_name':candy_name_txt,
        })
        vcommon.pout(ret)
