#!/bin/bash

source _common.sh

python3 src/luzi82/pkmgo/dbus_to_stdout.py luzi82.v11auto.video \
| python3 src/luzi82/pkmgo/memcache_to_stdout.py 127.0.0.1:11211 \
| python3 src/luzi82/pkmgo/image_crop_filter.py ${SCREEN_WIDTH} ${SCREEN_HEIGHT} ${SCREEN_CP_X} ${SCREEN_CP_Y} ${SCREEN_CP_W} ${SCREEN_CP_H} \
| python3 src/luzi82/pkmgo/image_grayscale_filter.py ${SCREEN_CP_WXH} \
| python3 src/luzi82/pkmgo/image_contrast_filter.py ${SCREEN_CP_WXH} 50 100 \
| python3 src/luzi82/pkmgo/tesseract_filter.py ${SCREEN_CP_W} ${SCREEN_CP_H}
