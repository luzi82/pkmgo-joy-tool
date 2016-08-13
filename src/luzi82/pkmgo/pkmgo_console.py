'''
Created on Aug 11, 2016

@author: luzi82
'''
import sys
import json
from luzi82.pkmgo import common as vcommon

from api import PokeAuthSession

session = None

def cmd_login(in_data):
    global session
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
        in_data['auth']
    )
    session = poko_session.authenticate(locationLookup="{},{}".format(in_data['lat'],in_data['long']))
    if not session:
        vcommon.perr('Session not created successfully')
        session = None
    vcommon.pout(json.dumps({
        "result":"success"
    }))

def cmd_move(in_data):
    global session
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
    global session
    good = True
    if 'radius' not in in_data:
        good = False
    if not good:
        vcommon.perr('ONHCIURH cmd not good')
        return
    map_object = session.getMapObjects(radius=in_data['radius'])
    ret = {
        "pokemon_list":[]
    }
    for map_cell in map_object.map_cells:
        pokemon_list = [p for p in map_cell.wild_pokemons]
        pokemon_list += [p.pokemon_data for p in map_cell.catchable_pokemons]
        for pokemon in pokemon_list:
            ret['pokemon_list'].append({
                "pokemonId":pokemon.pokemon_id,
                "lat":pokemon.latitude,
                "long":pokemon.longitude,
                "expiration_timestamp_ms":pokemon.expiration_timestamp_ms
            })
            
    vcommon.pout(json.dumps(ret))

CMD_DICT={
    'login':cmd_login,
    'move':cmd_move,
    'get_object':cmd_get_object
}

if __name__ == '__main__':

    if len(sys.argv) != 1:
        vcommon.perr ('{0}'.format(sys.argv[0]))
        exit()

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
