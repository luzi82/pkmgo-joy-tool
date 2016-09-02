#!/bin/bash

set -e

source ./_common.sh

python3 src/luzi82/pkmgo/dbus_to_stdout.py luzi82.pkmgo.drone_output \
| python3 src/luzi82/pkmgo/map_gather_filter.py \
| python3 src/luzi82/pkmgo/stdin_to_memcache.py 127.0.0.1:11211 musashi_map 1200
