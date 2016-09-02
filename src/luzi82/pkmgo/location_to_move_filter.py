'''
Created on Aug 28, 2016

@author: luzi82
'''

import sys,json
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr ('{0}'.format(sys.argv[0]))
        exit()
    
    for line in sys.stdin:
        data_json = line.rstrip('\n')
        data = None
        try:
            data = json.loads(data_json)
        except:
            continue
        
        out = {
            "cmd":"move",
            "lat":float(data['lat']),
            "lng":float(data['lng'])
        }
        vcommon.pout(json.dumps(out))
