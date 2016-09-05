'''
Created on Aug 11, 2016

@author: luzi82
'''
import argparse
import sys, time, traceback, random
import json
from luzi82.pkmgo import common as vcommon
from luzi82.pkmgo import config as vconfig
from luzi82.pkmgo import pkmgo_func

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    vconfig.add_argument(parser)
    args = parser.parse_args()

    config = vconfig.get(args)['config_dict']
    
    drone_update_list_sort = lambda x: -x['next_update']

    now_ms = int(time.time()*1000)
    drone_update_list = []
    step_up = int(config['get_object_period_min_ms'] / len(config['drone_dict']))
    drone_next_update = now_ms + step_up
    for drone_id in config['drone_dict']:
        drone_update_list.append({
            'drone_id':drone_id,
            'next_update':drone_next_update
        })
        drone_next_update += step_up

    drone_update_list=sorted(drone_update_list,key=drone_update_list_sort)

    while True:
        drone_update = drone_update_list.pop()
        data={
            "cmd":"get_object",
            'drone_id':drone_update['drone_id'],
            'timestamp_ms':drone_update['next_update'],
        }
        time.sleep(max(0.0001,(drone_update['next_update']/1000.)-time.time()))
        vcommon.pout(json.dumps(data))
        drone_update_list.append({
            'drone_id':drone_update['drone_id'],
            'next_update':drone_update['next_update']+random.randint(
                config['get_object_period_min_ms'],
                config['get_object_period_max_ms']
            ),
        })
        drone_update_list=sorted(drone_update_list,key=drone_update_list_sort)
