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

    config_dict = vconfig.get(args)['config_dict']
    drone_id_list = sorted(list(config_dict['drone_dict'].keys()))
    for k in drone_id_list:
        vcommon.pout(k)
