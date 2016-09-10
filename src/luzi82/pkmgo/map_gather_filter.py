'''
Created on Aug 28, 2016

@author: luzi82
'''

import sys,json,time,string,traceback
from luzi82.pkmgo import common as vcommon
from luzi82.pkmgo import pkmgo_func
from s2sphere import CellId
from pogo.location import Location

CLONE_LIST=[
    "s2_cell_id",
    "pokemon_id",
    "latitude",
    "longitude",
    "expiration_timestamp_ms",
]

MAP_ZOOM=17
MAP_WIDTH=640
MAP_HEIGHT=640

if __name__ == '__main__':
    if len(sys.argv) != 1:
        vcommon.perr ('{0}'.format(sys.argv[0]))
        exit()

    pokemon_dict = {}
    spawn_point_dict = {}
    drone_dict = {}
    maker_label_offset = 0
    center_latitude = 0
    center_longitude = 0

    map_long_width_256 = 360.*(0.5**MAP_ZOOM)
    map_long_width = MAP_WIDTH * map_long_width_256 / 256.
    map_long_width_half = map_long_width / 2.

    # gather
    for line in sys.stdin:
        if line == None:
            vcommon.perr('HCCEIFER line == None')
            break
        try:
            data_json = line.rstrip('\n')
            data = json.loads(data_json)
            
            # filter
            if 'cmd' not in data:
                vcommon.perr("cmd MJRVXSFU cmd not in data")
                continue
    
            # handle move
            if data['cmd'] == 'move':
                if data['result'] != 'success':
                    continue
                center_latitude = data['lat']
                center_longitude = data['lng']
                vcommon.perr("TKUJWBBV "+data_json)
                continue
            
            # filter
            if data['cmd'] != 'get_object':
                continue
            if data['result'] != 'success':
                continue

            now_ms = (int(time.time()*1000))
            discover_expiration_timestamp_ms = now_ms+30000

            # add
            for k,v in data['pokemon_dict'].items():
                if not k in pokemon_dict:
                    pokemon_dict[k] = {}
                    pokemon_dict[k]['maker_label'] = string.ascii_uppercase[maker_label_offset:maker_label_offset+1]
                    maker_label_offset += 1
                    maker_label_offset %= len(string.ascii_uppercase)
                pokemon = pokemon_dict[k]
                for key in CLONE_LIST:
                    if key in v:
                        pokemon[key] = v[key]
                pokemon['discover_expiration_timestamp_ms'] = discover_expiration_timestamp_ms

            # remove
            remove_list = []
            for k, pokemon in pokemon_dict.items():
                if ('expiration_timestamp_ms' in pokemon) and (pokemon['expiration_timestamp_ms'] <= now_ms):
                    remove_list.append(k)
                    continue
                if ('expiration_timestamp_ms' in pokemon) and (pokemon['expiration_timestamp_ms'] > now_ms):
                    continue
                if ('discover_expiration_timestamp_ms' in pokemon) and (pokemon['discover_expiration_timestamp_ms'] > now_ms):
                    continue
                remove_list.append(k)

            for k in remove_list:
                pokemon_dict.pop(k,None)

            # cal s2_cell_id
            for _, pokemon in pokemon_dict.items():
                if ( "s2_cell_id" in pokemon ) and ( "s2_latitude" not in pokemon ):
                    cell_id = CellId(pokemon["s2_cell_id"])
                    lat_lng = cell_id.to_lat_lng()
                    pokemon['s2_latitude'] = lat_lng.lat().degrees
                    pokemon['s2_longitude'] = lat_lng.lng().degrees

            nearby_dict = {}
            for _, pokemon in pokemon_dict.items():
                if ( "s2_cell_id" in pokemon ) and ( "latitude" not in pokemon ):
                    s2_cell_id = pokemon["s2_cell_id"]
                    if s2_cell_id not in nearby_dict:
                        cell_id = CellId(s2_cell_id)
                        lat_lng = cell_id.to_lat_lng()
                        nearby_dict[s2_cell_id] = {
                            'pokemon_list':[],
                            'cell_label':(str(s2_cell_id))[-1:],
                            'latitude':lat_lng.lat().degrees,
                            'longitude':lat_lng.lng().degrees,
                        }
                    nearby_pokemon_list = nearby_dict[s2_cell_id]['pokemon_list']
                    nearby_pokemon_list.append(pokemon)

            # spawn_point_dict add
            for spawn_point in data['spawn_point_list']:
                spawn_point['discover_expiration_timestamp_ms'] = discover_expiration_timestamp_ms
                spawn_point_dict[spawn_point['key']] = spawn_point

            # spawn_point_dict remove
            remove_list = []
            for k, spawn_point in spawn_point_dict.items():
                if ('discover_expiration_timestamp_ms' not in spawn_point):
                    remove_list.append(k)
                    continue
                if (spawn_point['discover_expiration_timestamp_ms'] <= now_ms):
                    remove_list.append(k)

            for k in remove_list:
                spawn_point_dict.pop(k,None)

            if data['drone_id'] not in drone_dict:
                drone_dict[data['drone_id']] = {}

            drone = drone_dict[data['drone_id']]
            drone['last_update_time_ms'] = data['time_ms']
            drone['latitude'] = data['lat']
            drone['longitude'] = data['lng']

            map_dist_width_half = Location.getDistance(
                center_latitude,center_longitude,
                center_latitude,center_longitude+map_long_width_half
            )
            latitude_n,_ = pkmgo_func.go(
                center_latitude,center_longitude,
                center_latitude+1,center_longitude,
                map_dist_width_half,0.1
            )
            latitude_s,_ = pkmgo_func.go(
                center_latitude,center_longitude,
                center_latitude-1,center_longitude,
                map_dist_width_half,0.1
            )

            output = {
                'center_latitude':center_latitude,
                'center_longitude':center_longitude,
                "nearby_dict":nearby_dict,
                "pokemon_dict":pokemon_dict,
                'spawn_point_dict':spawn_point_dict,
                'drone_dict':drone_dict,
                'latitude_n':latitude_n,
                'latitude_s':latitude_s,
                'longitude_w':center_longitude-map_long_width_half,
                'longitude_e':center_longitude+map_long_width_half,
            }
    
            vcommon.pout(json.dumps(output))
        except:
            vcommon.perr("WJQKOBST")
            traceback.print_exc()
