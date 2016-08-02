#!/bin/bash

source _common.sh

CLIP_X=264
CLIP_Y=474
CLIP_W=42
CLIP_H=19
CLIP_ZOOM=4

CLIP_ZOOM_W=$(expr ${CLIP_W} \* ${CLIP_ZOOM})
CLIP_ZOOM_H=$(expr ${CLIP_H} \* ${CLIP_ZOOM})
CLIP_BYTES=$(expr ${CLIP_W} \* ${CLIP_H} \* 3)
CLIP_ZOOM_BYTES=$(expr ${CLIP_ZOOM_W} \* ${CLIP_ZOOM_H} \* 3)

python3 src/luzi82/pkmgo/dbus_to_stdout.py luzi82.v11auto.video \
| python3 src/luzi82/pkmgo/memcache_to_stdout.py 127.0.0.1:11211 \
| python3 src/luzi82/pkmgo/image_crop_filter.py ${SCREEN_WIDTH} ${SCREEN_HEIGHT} ${CLIP_X} ${CLIP_Y} ${CLIP_W} ${CLIP_H} \
| python3 src/luzi82/pkmgo/image_zoom_filter.py ${CLIP_W} ${CLIP_H} ${CLIP_ZOOM} \
| python3 src/luzi82/pkmgo/image_grayscale_filter.py ${CLIP_ZOOM_BYTES} \
| python3 src/luzi82/pkmgo/image_contrast_filter.py ${CLIP_ZOOM_BYTES} 50 100 \
| python3 src/luzi82/pkmgo/tesseract_filter.py ${CLIP_ZOOM_W} ${CLIP_ZOOM_H}
