'''
Created on Jul 24, 2016

@author: luzi82
'''

import sys, string, random, time

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
