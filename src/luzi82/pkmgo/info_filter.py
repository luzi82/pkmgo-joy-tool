'''
Created on Jul 30, 2016

@author: luzi82
'''

import sys
import json
import re
from luzi82.pkmgo import common as vcommon

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr ('{0}'.format(sys.argv[0]))
        exit()
        
    cp_prog = re.compile('^CP(\d+)$')
    hp_prog = re.compile('^HP\d+/(\d+)$')
    powerup_stardust_prog = re.compile('^(\d+)$')
    powerup_candy_prog = re.compile('^(\d+)$')
    candy_name_prog = re.compile('^(.+) CANDY$')

    for line in sys.stdin:
        if line == None:
            vcommon.perr('CFHRVFSI byte_list == None')
            break
        info_json = line.rstrip('\n')
        info = json.loads(info_json)

        good = True

        cp_mo = cp_prog.match(info['cp'])
        if cp_mo == None: good = False
        hp_mo = hp_prog.match(info['hp'])
        if hp_mo == None: good = False
        powerup_stardust_mo = powerup_stardust_prog.match(info['powerup_stardust'])
        if powerup_stardust_mo == None: good = False
        powerup_candy_mo = powerup_candy_prog.match(info['powerup_candy'])
        if powerup_candy_mo == None: good = False
        candy_name_mo = candy_name_prog.match(info['candy_name'])
        if candy_name_mo == None: good = False
        
        if not good:
            vcommon.perr(info_json)
            continue
        
        out_json = json.dumps({
            'cp':int(cp_mo.group(1)),
            'hp':int(hp_mo.group(1)),
            'powerup_stardust':int(powerup_stardust_mo.group(1)),
            'powerup_candy':int(powerup_candy_mo.group(1)),
            'candy_name':candy_name_mo.group(1),
        })
        vcommon.pout(out_json)
