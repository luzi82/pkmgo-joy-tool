#!/bin/bash

source _common.sh

python3 src/luzi82/pkmgo/dbus_to_stdout.py luzi82.v11auto.video \
| python3 src/luzi82/pkmgo/memcache_to_stdout.py 127.0.0.1:11211 \
| python3 src/luzi82/pkmgo/frame_info_filter.py \
| python3 src/luzi82/pkmgo/info_filter.py \
| python3 src/luzi82/pkmgo/iv_calculation_filter.py \
| python3 src/luzi82/pkmgo/iv_beauty_filter.py
