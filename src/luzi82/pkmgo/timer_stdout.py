'''
Created on Aug 28, 2016

@author: luzi82
'''
import sys, time, json
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 3:
        vcommon.perr ('{0} ms msg_type'.format(sys.argv[0]))
        exit()
        
    arg_ms = int(sys.argv[1])
    arg_msg_type = sys.argv[2]
    
    while True:
        data = {"msg_type":arg_msg_type,"time":int(time.time()*1000)}
        vcommon.pout(json.dumps(data))
        time.sleep(arg_ms/1000.)
