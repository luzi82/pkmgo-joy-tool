'''
Created on Jul 31, 2016

@author: luzi82
'''

import sys, math
import json
from luzi82.pkmgo import iv_calculation_filter_data as my_data
from luzi82.pkmgo import common as vcommon

IV_RANGE = 16
EPSILON = 0.0001

LV_DATA_DICT_LIST=[]
for LV_CP_MULTIPLIER in my_data.LV_CP_MULTIPLIER_LIST:
    lv = LV_CP_MULTIPLIER[0]
    cp_multiplier = LV_CP_MULTIPLIER[1]
    stardust = 0
    for LV_STARDUST in my_data.LV_STARDUST_LIST:
        if LV_STARDUST[1] > lv:
            break
        stardust = LV_STARDUST[0]
    LV_DATA_DICT_LIST.append({
        'lv':lv,
        'cp_multiplier':cp_multiplier,
        'stardust':stardust,
    })

MONSTER_DATA_DICT_LIST=[
    {'name':x[0],'atk':x[1],'def':x[2],'sta':x[3],'candy':x[4]}
    for x in my_data.MONSTER_ATK_DEF_STA_CANDY_LIST
]

def cal_hp(mdd,ldd,stam_iv):
    return (mdd['sta']+stam_iv)*ldd['cp_multiplier']

def cal_cp(mdd,ldd,atk_iv,def_iv,stam_iv):
    return (mdd['atk']+atk_iv)*math.pow((mdd['def']+def_iv),0.5)*math.pow((mdd['sta']+stam_iv),0.5)*math.pow(ldd['cp_multiplier'],2)/10

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr('{0}'.format(sys.argv[0]))
        exit()
        
    for line in sys.stdin:
        if line == None:
            vcommon.perr('CFHRVFSI byte_list == None')
            break
        input_data_json = line.rstrip('\n')
        input_data = json.loads(input_data_json)
        
        hp_min = input_data['hp']-EPSILON
        hp_max = input_data['hp']+1+EPSILON
        if input_data['hp']==10: hp_min=0
        cp_min = input_data['cp']-EPSILON
        cp_max = input_data['cp']+1+EPSILON
        if input_data['cp']==10: cp_min=0
        
        match_list = []
        for mdd in MONSTER_DATA_DICT_LIST:
            if mdd['candy'] != input_data['candy_name']:continue
#             vcommon.perr('AJYYCVER '+mdd['candy'])
            for ldd in LV_DATA_DICT_LIST:
                if ldd['stardust'] != input_data['powerup_stardust']:continue
#                 vcommon.perr('SJAVZLIY '+str(ldd['stardust']))
                for stam_iv in range(IV_RANGE):
                    hp = cal_hp(mdd,ldd,stam_iv)
                    if (hp<hp_min)or(hp>hp_max):continue
#                     vcommon.perr('JXZKENCI '+str(hp))
                    for atk_iv in range(IV_RANGE):
                        for def_iv in range(IV_RANGE):
                            cp = cal_cp(mdd,ldd,atk_iv,def_iv,stam_iv)
                            if (cp<cp_min) or (cp>cp_max):continue
                            percent = (stam_iv+atk_iv+def_iv)/(IV_RANGE-1)/3
                            match_list.append({
                                'name':mdd['name'],
                                'percent':percent,
                                'atk':atk_iv,
                                'def':def_iv,
                                'sta':stam_iv,
                                'lv':ldd['lv'],
                            })

        out_json = json.dumps({
            'cp':input_data['cp'],
            'hp':input_data['hp'],
            'match_list':match_list
        })
        vcommon.pout(out_json)
