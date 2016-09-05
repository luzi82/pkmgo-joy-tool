#!/bin/bash

set -e

source ./_common.sh

python3 src/luzi82/pkmgo/get_object_stdout.py \
| python3 src/luzi82/pkmgo/stdin_to_dbus.py luzi82.pkmgo.drone_input /get_object
