#!/usr/bin/python

# luzi@gmail.com
# used for list pokemon only
# based on demo.py
# remove all user interaction

import argparse
import sys,time
import operator
import json

import POGOProtos.Enums.PokemonMove_pb2 as PokemonMove_pb2

from pogo.api import PokeAuthSession
from pogo.pokedex import pokedex
from luzi82.pkmgo import config
from luzi82.pkmgo import common as vcommon

# Entry point
# Start off authentication and demo
if __name__ == '__main__':
    # Read in args
    parser = argparse.ArgumentParser()
    config.add_argument(parser,['auth'])
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
        for line in sys.stdin:
            if line == None:
                vcommon.perr('GVNCGMTK byte_list == None')
                break
            in_data_json = line.rstrip('\n')
            in_data = None
            try:
                in_data = json.loads(in_data_json)
            except:
                vcommon.perr('KIMCRXOM bad json')
                continue
            for pid in in_data:
                vcommon.pout('XDERSFUL release %s'%(pid))
                session.releasePokemonId(pid)
                time.sleep(10)
    else:
        vcommon.perr('Session not created successfully')
        sys.exit(-1)
