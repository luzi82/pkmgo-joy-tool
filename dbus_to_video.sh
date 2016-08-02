#!/bin/bash

source _common.sh

python3 src/luzi82/pkmgo/dbus_to_stdout.py luzi82.v11auto.video \
| python3 src/luzi82/pkmgo/memcache_to_stdout.py 127.0.0.1:11211 \
| python3 src/luzi82/pkmgo/b64_to_bin.py \
| ffplay -framerate 60 -probesize 32 -fflags nobuffer -f rawvideo -pix_fmt bgr24 -s ${SCREEN_WIDTH}x${SCREEN_HEIGHT} -i -
