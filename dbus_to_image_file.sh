#!/bin/bash

source _common.sh

python3 src/luzi82/pkmgo/dbus_stdout.py luzi82.v11auto.video \
| python3 src/luzi82/pkmgo/memcache_stdout.py 127.0.0.1:11211 \
| python3 src/luzi82/pkmgo/b64_save_image.py ${SCREEN_WIDTH} ${SCREEN_HEIGHT} sample \
>> /dev/null
