#!/usr/bin/python

# luzi@gmail.com
# used for list pokemon only
# based on demo.py
# remove all user interaction

import argparse
import sys
import operator
import json

import POGOProtos.Enums.PokemonMove_pb2 as PokemonMove_pb2

from pogo.api import PokeAuthSession
from pogo.pokedex import pokedex
from luzi82.pkmgo import config
from luzi82.pkmgo import common as vcommon

def canEnvolve(pokemon_id):
    return pokedex.evolves[pokemon_id] > 0

def viewPokemon(session,file_output):
    party = session.inventory.party
    
    pkm_type_dict = {}
    for pokemon in party:
        #IvPercent = int(((pokemon.individual_attack + pokemon.individual_defense + pokemon.individual_stamina)*100)/45)
        cp = pokemon.cp

        pokemon_id = pokemon.pokemon_id
        if pokemon_id not in pkm_type_dict:
            pkm_type_dict[pokemon_id] = {'cp_list':[],'move_data_dict':{}}
        pkm_type = pkm_type_dict[pokemon_id]

        move_1 = pokemon.move_1
        move_2 = pokemon.move_2
        move_key = '%s_%s'%(move_1,move_2)
        if move_key not in pkm_type['move_data_dict']:
            pkm_type['move_data_dict'][move_key] = {'cp_list':[]}
        pkm_move_cp_list = pkm_type['move_data_dict'][move_key]['cp_list']
        
        pkm_type['cp_list'].append(cp)
        pkm_move_cp_list.append(cp)

    for _,v in pkm_type_dict.items():
        v['cp_list'] = sorted(v['cp_list'],reverse=True)
        for _,vv in v['move_data_dict'].items():
            vv['cp_list'] = sorted(vv['cp_list'],reverse=True)

    for _,v in pkm_type_dict.items():
        v['min_cp'] = v['cp_list'][min(len(v['cp_list'])-1,2)]
        for _,vv in v['move_data_dict'].items():
            vv['min_cp'] = vv['cp_list'][min(len(vv['cp_list'])-1,1)]

#     vcommon.pout(json.dumps(pkm_type_dict,indent=2))
    
    release_list = []
    
    myParty = []
    # Get the party and put it into a nicer list
    for pokemon in party:
        IvPercent = int(((pokemon.individual_attack + pokemon.individual_defense + pokemon.individual_stamina)*100)/45)
        # Get the names of the moves and remove the _FAST part of move 1
        move_1 = PokemonMove_pb2.PokemonMove.Name(pokemon.move_1)
        move_1 = move_1[:-5]
        move_2 = PokemonMove_pb2.PokemonMove.Name(pokemon.move_2)
        
        pid_key = pokemon.pokemon_id
        move_key = '%s_%s'%(pokemon.move_1,pokemon.move_2)
        min_cp = pkm_type_dict[pid_key]['min_cp'] if canEnvolve(pokemon.pokemon_id) else pkm_type_dict[pid_key]['move_data_dict'][move_key]['min_cp']
        release = (not pokemon.favorite) and (pokemon.cp < min_cp) and (IvPercent < 90)
        if release:
            release_list.append(pokemon.id)
        
        L = [
            pokedex[pokemon.pokemon_id],
            pokemon.cp,
            pokemon.individual_attack,
            pokemon.individual_defense,
            pokemon.individual_stamina,

            IvPercent,
            pokemon,
            move_1,
            move_2,
            pokemon.creation_time_ms,

            pokemon.favorite,
            pokemon.pokemon_id,
            -pokemon.cp,
            pokemon.id,
            release
        ]
        myParty.append(L)
    
    myParty.sort(key = operator.itemgetter(11,12))
    
    i = 0
    # Display the pokemon, with color coding for IVs and separation between types of pokemon
    vcommon.pout('ID                       | NAME            | R G F | CP    | IV% | MOVE 1          | MOVE 2')
    vcommon.pout('------------------------ | --------------- | ----- | ----- | --- | --------------- | --------------- ')
    for monster in myParty:
        if i == 3:
            vcommon.pout('')
            i = 0
        vcommon.pout(
            '%24s | %-15s | %-1s %-1s %-1s | %-5s | %-3s | %-15s | %-15s'%(
            monster[13],
            monster[0],
            ('R' if monster[14] else ' '),
            ('G' if monster[5]>90 else ' '),
            ('F' if monster[10] else ' '),
            monster[1],monster[5],
            monster[7],monster[8])
        )
        i = i+1
    
    vcommon.pout("release count: %s/%s"%(len(release_list),len(party)))
    
    with open(file_output, 'w') as outfile:
        json.dump(sorted(release_list),outfile)

# Entry point
# Start off authentication and demo
if __name__ == '__main__':
    # Read in args
    parser = argparse.ArgumentParser()
    config.add_argument(parser,['auth'])
    parser.add_argument("-o", "--output", help="File out", required=True)
    args = parser.parse_args()

    auth = config.get(args,['auth'])

    # Create PokoAuthObject
    poko_session = PokeAuthSession(
        auth['username'],
        auth['password'],
        auth['auth'],
        auth['encrypt_lib']
    )

    session = poko_session.authenticate()

    # Time to show off what we can do
    if session:
        session.getProfile()
        viewPokemon(session,args.output)
    else:
        vcommon.perr('Session not created successfully')
        sys.exit(-1)
