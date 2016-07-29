#!/bin/bash

source _common.sh

ffplay \
 -framerate 60 -probesize 32 -fflags nobuffer \
 -i "http://localhost:5656/?width=${SCREEN_WIDTH}&height=${SCREEN_HEIGHT}&bitRate=400000"
