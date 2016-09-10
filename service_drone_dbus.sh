#!/bin/bash

source _common.sh

while true; do
echo "MFVBVEHC drone bash start ${1}"
python3 src/luzi82/pkmgo/dbus_to_stdout.py luzi82.pkmgo.drone_input \
| python3 src/luzi82/pkmgo/drone.py -d ${1} \
| python3 src/luzi82/pkmgo/stdin_to_memcache_key.py 127.0.0.1:11211 1 \
| python3 src/luzi82/pkmgo/stdin_to_dbus.py luzi82.pkmgo.drone_output /drone_output_${1}
if [ "${PIPESTATUS[1]}" == "82" ];then
break
fi
done
