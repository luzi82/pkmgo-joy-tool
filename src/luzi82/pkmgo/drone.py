'''
Created on Aug 11, 2016

@author: luzi82
'''
import argparse
import sys, time, traceback, random
import json
from luzi82.pkmgo import common as vcommon
from luzi82.pkmgo import config as vconfig
from luzi82.pkmgo import pkmgo_func

from api import PokeAuthSession

runtime={
    "config":None,
    "drone_id":None,
    "drone_config":None,
    "session":None,
    "origin_lat":None,
    "origin_lng":None,
    "quit":False,
}

_FAIL = {'result':"fail"}

# def cmd_login(in_data):
#     global runtime
#     good = 'key' in in_data \
#         and 'lat' in in_data \
#         and 'lng' in in_data
#     if not good:
#         vcommon.perr('QMMNQQFG cmd not good')
#         return _FAIL
#     runtime['account_key'] = in_data['key']
#     runtime['origin_lat'] = in_data['lat']
#     runtime['origin_lng'] = in_data['lng']
#     try_login()
#     if runtime['session'] == None:
#         return _FAIL
#     return {'result':"success"}
# 
# def cmd_set_offset(in_data):
#     global runtime
#     good = 'offset_lat_meter' in in_data \
#         and 'offset_lng_meter' in in_data
#     if not good:
#         vcommon.perr('RNAKWCRL cmd not good')
#     runtime['offset_lat_meter'] = in_data['offset_lat_meter']
#     runtime['offset_lat_meter'] = in_data['offset_lat_meter']
#     return {'result':"success"}

def cmd_move(in_data):
    global runtime
    good = 'lat' in in_data \
        and 'lng' in in_data
    if not good:
        vcommon.perr('QMMNQQFG cmd not good')
        return _FAIL
    runtime['origin_lat'] = in_data['lat']
    runtime['origin_lng'] = in_data['lng']
    return {'result':"success"}

def cmd_get_object(in_data):
    global runtime
    if runtime['session'] == None:
        return None
    lat,lng = get_lat_lng()
    runtime['session'].location.setCoordinates(lat, lng)
    pokemon_dict = pkmgo_func.get_object(runtime['session'],runtime['config']['drone_radius'])
    return {'result':"success","pokemon_dict":pokemon_dict,"lat":lat,"lng":lng,"time_ms":int(time.time()*1000)}

def cmd_quit(in_data):
    global runtime
    runtime['quit'] = True
    return {'result':"success"}

def try_login():
    global runtime
    if runtime["origin_lat"] == None:
        return
    if runtime["origin_lng"] == None:
        return
    lat,lng = get_lat_lng()
    runtime['session'] = pkmgo_func.login(
        runtime['drone_config']['auth'],
        runtime['drone_config']['username'],
        runtime['drone_config']['password'],
        lat,lng,
        runtime['config']['encrypt_lib']
    )
    if not runtime['session']:
        vcommon.perr('Session not created successfully')
        runtime['session'] = None
        return
    j = {'msg_type':'drone_up'}
    j['drone_id'] = runtime['drone_id']
    vcommon.pout(json.dumps(j))

def get_lat_lng():
    global runtime
    if runtime['origin_lat'] == None:
        raise Exception('VFYRCFXL origin_lat none')
    if runtime['origin_lng'] == None:
        raise Exception('DIDTKTLG origin_lng none')
    lat,lng=pkmgo_func.offset(
        runtime['origin_lat'],runtime['origin_lng'],
        runtime['drone_config']['offset_lat_meter'],runtime['drone_config']['offset_lng_meter']
    )
    lat+=(random.random()*2-1)*runtime['config']['drone_vibrate_lat']
    lng+=(random.random()*2-1)*runtime['config']['drone_vibrate_lng']
    return lat,lng

CMD_DICT={
#     'login':cmd_login,
#     'set_offset':cmd_set_offset,
    'move':cmd_move,
    'get_object':cmd_get_object,
    'quit':cmd_quit,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    vconfig.add_argument(parser)
    parser.add_argument("-d", "--droneid", help="Drone ID", required=True)
    args = parser.parse_args()

    runtime['config'] = vconfig.get(args)['config_dict']
    runtime['drone_id'] = args.droneid
    runtime['drone_config'] = runtime['config']['drone_dict'][runtime['drone_id']]
    
    for line in sys.stdin:
        try:
            if line == None:
                vcommon.perr('CFHRVFSI line == None')
                break
            in_data_json = line.rstrip('\n')
            in_data = None
            try:
                in_data = json.loads(in_data_json)
            except:
                vcommon.perr('OSDETPEL bad json')
                continue
            if ( 'drone_id' in in_data ) and ( in_data['drone_id'] != runtime['drone_id'] ):
                continue
            if in_data['cmd'] not in CMD_DICT:
                vcommon.perr('CFHRVFSI cmd not in CMD_DICT')
                continue
            j = CMD_DICT[in_data['cmd']](in_data)
            if j != None:
                j.update(in_data)
                j['drone_id'] = runtime['drone_id']
                vcommon.pout(json.dumps(j))
        except:
            traceback.print_exc()
            runtime['session'] = None
            j = {'msg_type':'drone_down'}
            j['drone_id'] = runtime['drone_id']
            vcommon.pout(json.dumps(j))
        if runtime['session'] == None:
            try_login()
        if(runtime['quit']):
            break
