#!/bin/bash

set -e

echo '{"cmd":"reset"}' | python3 src/luzi82/pkmgo/stdin_to_dbus.py luzi82.pkmgo.drone_input /console
