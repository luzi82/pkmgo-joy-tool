#!/bin/bash

source _common.sh

rm -rf tmp

find sample/ | grep .png$ | sort \
| python3 src/luzi82/pkmgo/png_filename_to_rgb_filter.py \
| python3 src/luzi82/pkmgo/image_crop_filter.py ${SCREEN_WIDTH} ${SCREEN_HEIGHT} ${SCREEN_CP_X} ${SCREEN_CP_Y} ${SCREEN_CP_W} ${SCREEN_CP_H} \
| python3 src/luzi82/pkmgo/b64_to_png.py ${SCREEN_CP_W} ${SCREEN_CP_H} tmp \
