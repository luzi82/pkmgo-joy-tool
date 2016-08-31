#!/bin/bash

source _common.sh

python3 src/luzi82/pkmgo/drone.py -d 00 \
| python3 src/luzi82/pkmgo/map_gather_filter.py \
| python3 src/luzi82/pkmgo/stdin_to_memcache.py 127.0.0.1:11211 musashi_map 1200
