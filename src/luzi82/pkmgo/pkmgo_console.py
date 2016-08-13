'''
Created on Aug 11, 2016

@author: luzi82
'''
import argparse
import sys
import json
from luzi82.pkmgo import common as vcommon
from luzi82.pkmgo import config as vconfig

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
    print("map_cell_count: {}".format(len(map_object.map_cells)))
    for map_cell in map_object.map_cells:
        for pokemon in map_cell.wild_pokemons:
            print('pokemon_id: {}'.format(pokemon.pokemon_data.pokemon_id))
            print('latitude: {}'.format(pokemon.latitude))
            print('longitude: {}'.format(pokemon.longitude))
            print('time_till_hidden_ms: {}'.format(pokemon.time_till_hidden_ms))
        for pokemon in map_cell.catchable_pokemons:
            print('pokemon_id: {}'.format(pokemon.pokemon_id))
            print('latitude: {}'.format(pokemon.latitude))
            print('longitude: {}'.format(pokemon.longitude))
            print('expiration_timestamp_ms: {}'.format(pokemon.expiration_timestamp_ms))
        for pokemon in map_cell.nearby_pokemons:
            print('pokemon_id: {}'.format(pokemon.pokemon_id))
            print('distance_in_meters: {}'.format(pokemon.distance_in_meters))
#             print(type(pokemon))
#             print(dir(pokemon))
#             p = pokemon
#             if hasattr(pokemon, 'pokemon_data'):
#                 p = pokemon.pokemon_data
#             ret['pokemon_list'].append({
#                 "pokemonId":p.pokemon_id,
#                 "lat":p.latitude,
#                 "long":p.longitude,
#                 "expiration_timestamp_ms":p.expiration_timestamp_ms
#             })
            
    vcommon.pout(json.dumps(ret))

CMD_DICT={
    'login':cmd_login,
    'move':cmd_move,
    'get_object':cmd_get_object
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
