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
from collections import deque

from api import PokeAuthSession

runtime={
    "config":None,
    "drone_id":None,
    "drone_config":None,
    "session":None,
    "origin_lat":None,
    "origin_lng":None,
    "quit":False,
    "get_object_enable":True,
    'encounter_history_queue':deque(),
    'last_api_timestamp':0,
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
    pout({'result':"success"},in_data)

def cmd_get_object(in_data):
    global runtime
    if not runtime['get_object_enable']:
        return None
    login()
    if runtime['session'] == None:
        return None
    lat,lng = get_lat_lng()
    runtime['session'].location.setCoordinates(lat, lng)
    wait_api()
    ret = pkmgo_func.get_object(runtime['session'],runtime['config']['drone_radius'])
    wait_api_mark()
    runtime['last_api_timestamp'] = int(time.time()*1000)
    ret.update({'result':"success",'type':'map',"lat":lat,"lng":lng,"time_ms":int(time.time()*1000)})
    pout(ret,in_data)
    for _,pokemon in ret['pokemon_dict'].items():
        if 'encounter_id' not in pokemon:
            continue
        if 'spawn_point_id' not in pokemon:
            continue
        if pokemon['encounter_id'] in runtime['encounter_history_queue']:
            continue
        runtime['encounter_history_queue'].append(pokemon['encounter_id'])
        wait_api()
        encounter = runtime['session'].encounterPokemonById(pokemon['encounter_id'],pokemon['spawn_point_id'])
        wait_api_mark()
        ret = {
            'result':"success",'type':'encounter',
            'encounter_id':pokemon['encounter_id'],
            'individual_attack':encounter.wild_pokemon.pokemon_data.individual_attack,
            'individual_defense':encounter.wild_pokemon.pokemon_data.individual_defense,
            'individual_stamina':encounter.wild_pokemon.pokemon_data.individual_stamina,
        }
        pout(ret,in_data)
    while len(runtime['encounter_history_queue'])>runtime['config']['encounter_history_queue_size']:
        runtime['encounter_history_queue'].popleft()

def cmd_quit(in_data):
    global runtime
    runtime['quit'] = True
    pout({'result':"success"},in_data)

def cmd_reset(in_data):
    exit(1)

def cmd_set_get_object_enable(in_data):
    global runtime
    if 'enable' not in in_data:
        vcommon.perr('YKJFEEHKOE cmd not good')
        return _FAIL
    runtime['get_object_enable'] = in_data['enable']
    pout({'result':"success"},in_data)

def login():
    global runtime
    if runtime["session"] != None:
        return
    if runtime["origin_lat"] == None:
        return
    if runtime["origin_lng"] == None:
        return
    lat,lng = get_lat_lng()
    wait_api()
    runtime['session'] = pkmgo_func.login(
        runtime['drone_config']['auth'],
        runtime['drone_config']['username'],
        runtime['drone_config']['password'],
        lat,lng,
        runtime['config']['encrypt_lib']
    )
    wait_api_mark()
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

def pout(j,in_data):
    global runtime
    if j == None:
        return
    j.update(in_data)
    j['drone_id'] = runtime['drone_id']
    vcommon.pout(json.dumps(j))

def wait_api():
    global runtime
    delay_ms = runtime['last_api_timestamp']+runtime['config']['encounter_delay_ms']-int(time.time()*1000)
    if delay_ms > 0:
        time.sleep(delay_ms/1000.)

def wait_api_mark():
    global runtime
    runtime['last_api_timestamp'] = int(time.time()*1000)

CMD_DICT={
#     'login':cmd_login,
#     'set_offset':cmd_set_offset,
    'move':cmd_move,
    'get_object':cmd_get_object,
    'quit':cmd_quit,
    'reset':cmd_reset,
    'set_get_object_enable':cmd_set_get_object_enable,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    vconfig.add_argument(parser)
    parser.add_argument("-d", "--droneid", help="Drone ID", required=True)
    args = parser.parse_args()

    runtime['config'] = vconfig.get(args)['config_dict']
    runtime['drone_id'] = args.droneid
    runtime['drone_config'] = runtime['config']['drone_dict'][runtime['drone_id']]

    j = {'msg_type':'drone_start'}
    j['drone_id'] = runtime['drone_id']
    vcommon.pout(json.dumps(j))

    try:
        for line in sys.stdin:
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
            CMD_DICT[in_data['cmd']](in_data)
#             if j != None:
#                 j.update(in_data)
#                 j['drone_id'] = runtime['drone_id']
#                 vcommon.pout(json.dumps(j))
            if(runtime['quit']):
                exit(82)
    except KeyboardInterrupt:
        runtime['session'] = None
        j = {'msg_type':'drone_down'}
        j['drone_id'] = runtime['drone_id']
        vcommon.pout(json.dumps(j))
        exit(82)
    except SystemExit as se:
        runtime['session'] = None
        j = {'msg_type':'drone_down'}
        j['drone_id'] = runtime['drone_id']
        vcommon.pout(json.dumps(j))
        raise se
    except:
        traceback.print_exc()
        runtime['session'] = None
        j = {'msg_type':'drone_down'}
        j['drone_id'] = runtime['drone_id']
        vcommon.pout(json.dumps(j))
        exit(-1)
