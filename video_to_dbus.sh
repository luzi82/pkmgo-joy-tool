#!/bin/bash

source _common.sh

ffmpeg \
 -nostats -framerate 60 -probesize 32 -fflags nobuffer \
 -i "http://localhost:5656/?width=${SCREEN_WIDTH}&height=${SCREEN_HEIGHT}&bitRate=400000" \
 -pix_fmt bgr24 -f rawvideo -vcodec rawvideo pipe:1 \
| python3 src/luzi82/pkmgo/bin_split_b64.py ${SCREEN_WXH} \
| python3 src/luzi82/pkmgo/skip_filter.py 2 \
| python3 src/luzi82/pkmgo/mean_filter.py ${SCREEN_WXH} 10 \
| python3 src/luzi82/pkmgo/stdin_to_memcache_key.py 127.0.0.1:11211 10 \
| python3 src/luzi82/pkmgo/stdin_to_dbus.py luzi82.v11auto.video /video_input

# | python3 src/luzi82/pkmgo/stdin_time_filter.py 1000 \
# | python3 src/luzi82/pkmgo/mean_filter.py ${SCREEN_WXH} 20 \
