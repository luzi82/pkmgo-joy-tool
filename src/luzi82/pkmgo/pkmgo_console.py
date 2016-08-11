'''
Created on Aug 11, 2016

@author: luzi82
'''
import argparse
from luzi82.pkmgo import auth_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    auth_config.add_argument(parser)
    parser.add_argument("-s", "--sort", help="Sort order", required=False)
    args = parser.parse_args()
