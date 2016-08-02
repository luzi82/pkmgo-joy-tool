'''
Created on Jul 29, 2016

@author: luzi82
'''

import sys
import base64, codecs
from luzi82.pkmgo import common as vcommon

from_codec_func_dict = {
    'base64':base64.b64decode,
    'hex':bytes.fromhex,
}

def decode_utf8_func(func):
    def ret_func(data):
        return func(data).decode('utf-8')
    return ret_func

def to_hex(data):
    return codecs.encode(data,'hex')

to_codec_func_dict = {
    'base64':decode_utf8_func(base64.b64encode),
    'hex':decode_utf8_func(to_hex),
}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        vcommon.perr('{0} from to'.format(sys.argv[0]))
        exit()
    
    arg_from = sys.argv[1]
    arg_to = sys.argv[2]
    
    from_codec_func = from_codec_func_dict[arg_from]
    to_codec_func = to_codec_func_dict[arg_to]
    
    for line in sys.stdin:
        if line == None:
            vcommon.perr('EFDFGUJL byte_list == None')
            break
        l = line.rstrip('\n')
        data = from_codec_func(l)
        ret = to_codec_func(data)
        vcommon.pout(ret)
