'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys, string, random, time

SCREEN_WIDTH=360
SCREEN_HEIGHT=640

SCREEN_CP_X=113
SCREEN_CP_Y=37
SCREEN_CP_W=121
SCREEN_CP_H=31

SCREEN_HP_X=107
SCREEN_HP_Y=314
SCREEN_HP_W=150
SCREEN_HP_H=19

SCREEN_POWERUP_STARDUST_X=196
SCREEN_POWERUP_STARDUST_Y=474
SCREEN_POWERUP_STARDUST_W=50
SCREEN_POWERUP_STARDUST_H=19

SCREEN_POWERUP_CANDY_X=264
SCREEN_POWERUP_CANDY_Y=474
SCREEN_POWERUP_CANDY_W=42
SCREEN_POWERUP_CANDY_H=19

SCREEN_CANDY_NAME_X=177
SCREEN_CANDY_NAME_Y=433
SCREEN_CANDY_NAME_W=139
SCREEN_CANDY_NAME_H=19

SCREEN_PIX_COUNT = SCREEN_WIDTH*SCREEN_HEIGHT
SCREEN_BYTE_COUNT = SCREEN_PIX_COUNT*3

CONTRAST_MIN = 0.5
CONTRAST_MAX = 1.

def pout(message):
    pp(message,sys.stdout)

def perr(message):
    pp(message,sys.stderr)

def pp(message,file):
    print(message,file=file)
    file.flush()

rand_key_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
def gen_key():
    return ("".join(random.choice(rand_key_charset)for _ in range(50)))+str(int(time.time()*1000))

def combine_dict(dist_list):
    ret = {}
    for dist in dist_list:
        ret.update(dist)
    return ret
