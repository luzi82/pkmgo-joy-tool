'''
Created on Aug 11, 2016

@author: luzi82
'''
import argparse
import sys, time
import json
from luzi82.pkmgo import common as vcommon
from luzi82.pkmgo import config as vconfig
from luzi82.pkmgo import pkmgo_func

from api import PokeAuthSession

config = None
session = None

def cmd_login(in_data):
    global session, config
    good = True
    if 'username' not in in_data:
        good = False
    if 'password' not in in_data:
        good = False
    if 'auth' not in in_data:
        good = False
    if 'lat' not in in_data:
        good = False
    if 'long' not in in_data:
        good = False
    if not good:
        vcommon.perr('CFGOVAPX cmd not good')
        return
    poko_session = PokeAuthSession(
        in_data['username'],
        in_data['password'],
        in_data['auth'],
        config['encrypt_lib']
    )
    session = poko_session.authenticate(locationLookup="{},{}".format(in_data['lat'],in_data['long']))
    if not session:
        vcommon.perr('Session not created successfully')
        session = None
    vcommon.pout(json.dumps({
        "result":"success"
    }))

def cmd_move(in_data):
    global session, config
    good = True
    if 'lat' not in in_data:
        good = False
    if 'long' not in in_data:
        good = False
    if not good:
        vcommon.perr('YVOWERWW cmd not good')
        return
    session.location.setCoordinates(in_data['lat'], in_data['long'])
    vcommon.pout(json.dumps({
        "result":"success"
    }))
    
def cmd_get_object(in_data):
    global session, config
    radius = 2
    if 'radius' in in_data:
        radius = in_data['radius']
    cell_list = None
    if 'cell_list' in in_data:
        cell_list = in_data['cell_list']
    map_object = session.getMapObjects(radius=radius,cells=cell_list)
    pokemon_dict = pkmgo_func.get_pokemon_dict(map_object)
            
    vcommon.pout(json.dumps(pokemon_dict,sort_keys=True,indent=2))

def interpo(out0,out1,in0,in1,i):
    return out0+(out1-out0)*(i-in0)/(in1-in0)

def cmd_check_detection(in_data):
    global session, config
    good = 'lat' in in_data and \
        'long' in in_data and \
        'encounter_id' in in_data and \
        'distance' in in_data and \
        'tick' in in_data and \
        'radius' in in_data and \
        'delay' in in_data
    if not good:
        vcommon.perr('QTSPYMZB cmd not good')
        return
    tick = in_data['tick']
    encounter_id = in_data['encounter_id']
    map_object = session.getMapObjects(radius=in_data['radius'])
    lat_max,_=pkmgo_func.go(in_data['lat'],in_data['long'],in_data['lat']+0.1,in_data['long'],100,1)
    lat_min,_=pkmgo_func.go(in_data['lat'],in_data['long'],in_data['lat']-0.1,in_data['long'],100,1)
    _,long_max=pkmgo_func.go(in_data['lat'],in_data['long'],in_data['lat'],in_data['long']+0.1,100,1)
    _,long_min=pkmgo_func.go(in_data['lat'],in_data['long'],in_data['lat'],in_data['long']-0.1,100,1)
    ret = []
    deadline = None
    for lati in range(tick):
        for longi in range(tick):
            if ( deadline != None ) and ( time.time()*1000 > deadline ):
                continue
            time.sleep(in_data['delay']/1000)
            lat = interpo(lat_min,lat_max,0,tick-1,lati)
            long = interpo(long_min,long_max,0,tick-1,longi)
            session.location.setCoordinates(lat, long)
            map_object = session.getMapObjects(radius=in_data['radius'])
            pokemon_dict = pkmgo_func.get_pokemon_dict(map_object)
            p = {'lat':lat,'long':long,'wild':False,'catchable':False,'nearby':False}
            if encounter_id in pokemon_dict:
                pokemon = pokemon_dict[encounter_id]
                p['wild']=pokemon['wild']
                p['catchable']=pokemon['catchable']
                p['nearby']=pokemon['nearby']
                if 'time_till_hidden_ms' in pokemon:
                    deadline = time.time()*1000 + pokemon['time_till_hidden_ms'] - 10000
            ret.append(p)
            vcommon.pout(json.dumps(p))
    vcommon.pout(json.dumps(ret,sort_keys=True,indent=2))

CMD_DICT={
    'login':cmd_login,
    'move':cmd_move,
    'get_object':cmd_get_object,
    'check_detection':cmd_check_detection,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    vconfig.add_argument(parser)
    args = parser.parse_args()

    config = vconfig.get(args)

    for line in sys.stdin:
        if line == None:
            vcommon.perr('CFHRVFSI byte_list == None')
            break
        in_data_json = line.rstrip('\n')
        in_data = None
        try:
            in_data = json.loads(in_data_json)
        except:
            vcommon.perr('OSDETPEL bad json')
            continue
        if in_data['cmd'] not in CMD_DICT:
            vcommon.perr('CFHRVFSI byte_list == None')
            continue
        CMD_DICT[in_data['cmd']](in_data)
