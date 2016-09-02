#!/bin/bash

set -e

source ./_common.sh

python3 src/luzi82/pkmgo/timer_stdout.py 10000 asdf \
| python3 src/luzi82/pkmgo/const_filter.py '{"cmd":"get_object"}' \
| python3 src/luzi82/pkmgo/stdin_to_dbus.py luzi82.pkmgo.drone_input /get_object
