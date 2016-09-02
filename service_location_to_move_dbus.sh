#!/bin/bash

set -e

source _common.sh

python3 src/luzi82/pkmgo/timer_stdout.py 1000 x \
| python3 src/luzi82/pkmgo/const_filter.py musashi_location \
| python3 src/luzi82/pkmgo/memcache_to_stdout.py 127.0.0.1:11211 \
| python3 src/luzi82/pkmgo/location_to_move_filter.py \
| python3 src/luzi82/pkmgo/stdin_to_dbus.py luzi82.pkmgo.drone_input /service_location_to_move_dbus
