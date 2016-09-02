#!/bin/bash

source _common.sh

python3 src/luzi82/pkmgo/dbus_to_stdout.py luzi82.pkmgo.drone_input \
| python3 src/luzi82/pkmgo/drone.py -d ${1} \
| python3 src/luzi82/pkmgo/stdin_to_dbus.py luzi82.pkmgo.drone_output /drone_output