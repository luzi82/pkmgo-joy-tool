#!/bin/bash

export PYTHONPATH=${PWD}/src/:${PWD}/third-party/pokemongo-api/pogo/
export SCREEN_WIDTH=360
export SCREEN_HEIGHT=640
export SCREEN_CP_X=99
export SCREEN_CP_Y=37
export SCREEN_CP_W=156
export SCREEN_CP_H=31

export SCREEN_WXH=$(expr ${SCREEN_WIDTH} \* ${SCREEN_HEIGHT} \* 3)
export SCREEN_CP_WXH=$(expr ${SCREEN_CP_W} \* ${SCREEN_CP_H} \* 3)
