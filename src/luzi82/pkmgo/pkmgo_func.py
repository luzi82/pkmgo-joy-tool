'''
Created on Aug 13, 2016

@author: luzi82
'''

from pogo.location import Location
import s2sphere

import sys, time
import json
from luzi82.pkmgo import common as vcommon
from luzi82.pkmgo import config as vconfig

from api import PokeAuthSession

def get_pokemon_dict(map_object):
    pokemon_dict={}
    
    def get_pokemon(pokemon_dict,encounter_id):
        if encounter_id not in pokemon_dict:
            pokemon_dict[encounter_id]={}
            pokemon_dict[encounter_id]['encounter_id']=encounter_id
            pokemon_dict[encounter_id]['wild']=False
            pokemon_dict[encounter_id]['catchable']=False
            pokemon_dict[encounter_id]['nearby']=False
            pokemon_dict[encounter_id]['from_pokestop']=False
        return pokemon_dict[encounter_id]
    
    for map_cell in map_object.map_cells:
        for pokemon in map_cell.wild_pokemons:
            p = get_pokemon(pokemon_dict,pokemon.encounter_id)
            p['s2_cell_id']=map_cell.s2_cell_id
            p['pokemon_id']=pokemon.pokemon_data.pokemon_id
            p['latitude']=pokemon.latitude
            p['longitude']=pokemon.longitude
            p['time_till_hidden_ms']=pokemon.time_till_hidden_ms
            p['wild']=True
        for pokemon in map_cell.catchable_pokemons:
            p = get_pokemon(pokemon_dict,pokemon.encounter_id)
            p['s2_cell_id']=map_cell.s2_cell_id
            p['pokemon_id']=pokemon.pokemon_id
            p['latitude']=pokemon.latitude
            p['longitude']=pokemon.longitude
            p['expiration_timestamp_ms']=pokemon.expiration_timestamp_ms
            p['catchable']=True
        for pokemon in map_cell.nearby_pokemons:
            p = get_pokemon(pokemon_dict,pokemon.encounter_id)
            p['s2_cell_id']=map_cell.s2_cell_id
            p['pokemon_id']=pokemon.pokemon_id
            p['distance_in_meters']=pokemon.distance_in_meters
            p['nearby']=True
        for fort in map_cell.forts:
            if fort.lure_info.lure_expires_timestamp_ms == 0:
                continue
            p = get_pokemon(pokemon_dict,fort.lure_info.encounter_id)
            p['s2_cell_id']=map_cell.s2_cell_id
            p['pokemon_id']=fort.lure_info.active_pokemon_id
            p['latitude']=fort.latitude
            p['longitude']=fort.longitude
            p['expiration_timestamp_ms']=fort.lure_info.lure_expires_timestamp_ms
            p['from_pokestop']=True

    return pokemon_dict

def get_spawn_point_list(map_object):
    ret = []
    
    for map_cell in map_object.map_cells:
        for spawn_point in map_cell.spawn_points:
            ret.append({
                'key':'{}-{}'.format(spawn_point.latitude,spawn_point.longitude),
                's2_cell_id':map_cell.s2_cell_id,
                'latitude':spawn_point.latitude,
                'longitude':spawn_point.longitude,
            })

    return ret

def get_fort_list(map_object):
    ret = []

    for map_cell in map_object.map_cells:
        for fort in map_cell.forts:
            ret.append({
                'fort_id':fort.id,
                'fort_type':fort.type,
                'latitude':fort.latitude,
                'longitude':fort.longitude,
                'sakura':fort.lure_info.lure_expires_timestamp_ms != 0,
            })

    return ret

def go(lat0,long0,lat1,long1,distance,epsilon):
    diff = Location.getDistance(lat0,long0,lat1,long1)-distance
    if (diff < 0) or abs(diff) < epsilon:
        return lat1,long1
    lat00 = lat0
    long00 = long0
    while True:
        latm = (lat0+lat1)/2
        longm = (long0+long1)/2
        diff = Location.getDistance(lat00,long00,latm,longm)-distance
        if abs(diff) < epsilon:
            return latm,longm
        if diff < 0:
            lat0 = latm
            long0 = longm
        else:
            lat1 = latm
            long1 = longm

def get_cell_neighbors(cell_id,radius=1):
#     cellid = s2sphere.CellId(cell_id)
    level = cell_id.level()
    size = cell_id.get_size_ij(level)
    face, i, j, _ = cell_id.to_face_ij_orientation()

    ret=[]
    for ii in range(-radius,radius+1):
        for jj in range(-radius,radius+1):
            new_i=i+(ii*size)
            new_j=j+(jj*size)
            same_face=(new_i>=0) and (new_i<cell_id.__class__.MAX_SIZE) and \
                (new_j>=0) and (new_j<cell_id.__class__.MAX_SIZE)
            ret.append(cell_id.from_face_ij_same(face,new_i,new_j,same_face))
    
    return ret

def login(auth,username,password,lat,lng,encrypt_lib):
    poko_session = PokeAuthSession(username,password,auth,encrypt_lib)
    session = poko_session.authenticate(locationLookup="{},{}".format(lat,lng))
    return session

def get_object(session,cell_radius):
    map_object = session.getMapObjects(radius=cell_radius)
    ret = {}
    ret['pokemon_dict'] = get_pokemon_dict(map_object)
    ret['spawn_point_list'] = get_spawn_point_list(map_object)
    ret['fort_list'] = get_fort_list(map_object)
    return ret

def offset(lat,lng,lat_meter,lng_meter):
    if lat_meter > 0:
        lat,lng=go(lat,lng,lat+0.1,lng,lat_meter,0.1)
    elif lat_meter < 0:
        lat,lng=go(lat,lng,lat-0.1,lng,-lat_meter,0.1)
    if lng_meter > 0:
        lat,lng=go(lat,lng,lat,lng+0.1,lng_meter,0.1)
    elif lng_meter < 0:
        lat,lng=go(lat,lng,lat,lng-0.1,-lng_meter,0.1)
    return lat,lng
