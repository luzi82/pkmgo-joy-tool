#!/usr/bin/python

# luzi@gmail.com
# used for list pokemon only
# based on demo.py
# remove all user interaction

import argparse
import sys
import operator

import POGOProtos.Enums.PokemonMove_pb2 as PokemonMove_pb2

from pogo.api import PokeAuthSession
from pogo.pokedex import pokedex
from luzi82.pkmgo import auth_config
from luzi82.pkmgo import common as vcommon

def viewPokemon(session,aSort):
    party = session.inventory.party
    myParty = []
    
    # Get the party and put it into a nicer list
    for pokemon in party:
        IvPercent = int(((pokemon.individual_attack + pokemon.individual_defense + pokemon.individual_stamina)*100)/45)
        # Get the names of the moves and remove the _FAST part of move 1
        move_1 = PokemonMove_pb2.PokemonMove.Name(pokemon.move_1)
        move_1 = move_1[:-5]
        move_2 = PokemonMove_pb2.PokemonMove.Name(pokemon.move_2)
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
            -pokemon.cp
        ]
        myParty.append(L)
    
    if aSort == 'recent':
        myParty.sort(key = operator.itemgetter(9))
        myParty = reversed(myParty)
    elif aSort == 'iv':
        myParty.sort(key = operator.itemgetter(5))
        myParty = reversed(myParty)
    elif aSort == 'number':
        myParty.sort(key = operator.itemgetter(11,12))
    
    i = 0
    # Display the pokemon, with color coding for IVs and separation between types of pokemon
    vcommon.pout(' NAME            | G F | CP    | ATK | DEF | STA | IV% | MOVE 1          | MOVE 2')
    vcommon.pout('---------------- | --- | ----- | --- | --- | --- | --- | --------------- | --------------- ')
    for monster in myParty:
        if i == 3:
            vcommon.pout('')
            i = 0
        vcommon.pout(
            ' %-15s | %-1s %-1s | %-5s | %-3s | %-3s | %-3s | %-3s | %-15s | %-15s | %-15s'%(
            monster[0],
            ('G' if monster[5]>90 else ' '),
            ('F' if monster[10] else ' '),
            monster[1],
            monster[2],monster[3],monster[4],monster[5],monster[7],monster[8],monster[9])
        )
        i = i+1

# Entry point
# Start off authentication and demo
if __name__ == '__main__':
    # Read in args
    parser = argparse.ArgumentParser()
    auth_config.add_argument(parser)
    parser.add_argument("-s", "--sort", help="Sort order", required=False)
    args = parser.parse_args()

    auth = auth_config.get_auth(args)
    if args.sort == None:
        args.sort = 'recent'
    if args.sort not in ['recent','iv','number']:
        vcommon.perr('Invalid sort {}'.format(args.sort))
        sys.exit(-1)

    # Create PokoAuthObject
    poko_session = PokeAuthSession(
        auth['username'],
        auth['password'],
        auth['auth']
    )

    session = poko_session.authenticate()

    # Time to show off what we can do
    if session:
        session.getProfile()
        viewPokemon(session,args.sort)
    else:
        vcommon.perr('Session not created successfully')
        sys.exit(-1)
