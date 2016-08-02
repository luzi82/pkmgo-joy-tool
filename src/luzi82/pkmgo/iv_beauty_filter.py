'''
Created on Aug 1, 2016

@author: luzi82
'''

import sys, math
import json
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr ('{0}'.format(sys.argv[0]))
        exit()

    for line in sys.stdin:
        if line == None:
            vcommon.perr('CFHRVFSI byte_list == None')
            break
        in_data_json = line.rstrip('\n')
        in_data = json.loads(in_data_json)
        
        match_list = in_data['match_list']
        
        name_list = []
        for match in match_list:
            name = match['name']
            if name not in name_list:
                name_list.append(name)
        
        if len(name_list)>0:
            vcommon.pout('==============================================')

        for name in reversed(name_list):
            variance = 0
            max_atk = -1
            min_atk = 999
            max_def = -1
            min_def = 999
            max_sta = -1
            min_sta = 999
            max_percent = -1
            min_percent = 999
            max_0_percent = -1
            min_0_percent = 999
            mean_0_percent = 0
            mean_0_count = 0
            for match in match_list:
                if match['name'] != name: continue
                variance += 1
                max_atk = max(match['atk'],max_atk)
                min_atk = min(match['atk'],min_atk)
                max_def = max(match['def'],max_def)
                min_def = min(match['def'],min_def)
                max_sta = max(match['sta'],max_sta)
                min_sta = min(match['sta'],min_sta)
                max_percent = max(match['percent'],max_percent)
                min_percent = min(match['percent'],min_percent)
                if math.floor(match['lv']) == match['lv']:
                    max_0_percent = max(match['percent'],max_0_percent)
                    min_0_percent = min(match['percent'],min_0_percent)
                    mean_0_percent += match['percent']
                    mean_0_count = mean_0_count + 1
        
            if mean_0_count == 0:
                mean_0_count = 1
            mean_0_percent = mean_0_percent / mean_0_count
        
            vcommon.pout('  CP: {0}'.format(in_data['cp']))
            vcommon.pout('  HP: {0}'.format(in_data['hp']))
            vcommon.pout('NAME: {0}'.format(name))
            vcommon.pout('  0%: {0:02.2f}-{1:02.2f} {2:02.2f}'.format(min_0_percent,max_0_percent,mean_0_percent))
            vcommon.pout('   %: {0:02.2f}-{1:02.2f}'.format(min_percent,max_percent))
            vcommon.pout(' VAR: {0}'.format(variance))
            vcommon.pout(' ATK: {0}-{1}'.format(min_atk,max_atk))
            vcommon.pout(' DEF: {0}-{1}'.format(min_def,max_def))
            vcommon.pout(' STA: {0}-{1}'.format(min_sta,max_sta))
            vcommon.pout('-------------------------')
