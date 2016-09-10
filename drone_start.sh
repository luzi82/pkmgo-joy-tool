#!/bin/bash

set -e

SCREENRC_FILE=/tmp/service_drone_dbus.screenrc

DRONE_LIST=`python3 src/luzi82/pkmgo/list_drone_id.py`
SCREEN_ID=0

rm -rf ${SCREENRC_FILE}

for drone_id in ${DRONE_LIST}; do
  echo screen ${SCREEN_ID} ./service_drone_dbus.sh ${drone_id} >> ${SCREENRC_FILE}
  SCREEN_ID=`expr 1 + ${SCREEN_ID}`
done
echo "detach" >> ${SCREENRC_FILE}

screen -S service_drone_dbus -c ${SCREENRC_FILE}

rm -rf ${SCREENRC_FILE}
