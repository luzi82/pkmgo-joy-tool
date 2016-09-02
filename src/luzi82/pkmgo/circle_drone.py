'''
Created on 2 Sep 2016

@author: luzi
'''

import sys, time, math
from luzi82.pkmgo import common as vcommon
import urllib.request

if __name__ == '__main__':
    if len(sys.argv) != 8:
        vcommon.perr ('{0} url_prefix lat_min lng_min lat_max lng_max loop_time_ms call_time_ms'.format(sys.argv[0]))
        exit()
        
    arg_url_prefix = sys.argv[1]
    arg_lat_min = float(sys.argv[2])
    arg_lng_min = float(sys.argv[3])
    arg_lat_max = float(sys.argv[4])
    arg_lng_max = float(sys.argv[5])
    arg_loop_time_ms = int(sys.argv[6])
    arg_call_time_ms = int(sys.argv[7])
    
    while True:
        t = int(time.time()*1000)
        angle = ((t%arg_loop_time_ms)/float(arg_loop_time_ms))*math.pi*2
        #vcommon.perr(angle)
        #vcommon.perr(math.cos(angle))
        lat = arg_lat_min + (arg_lat_max-arg_lat_min)*(0.5+0.5*math.cos(angle))
        lng = arg_lng_min + (arg_lng_max-arg_lng_min)*(0.5+0.5*math.sin(angle))
        url = arg_url_prefix+"?lat={}&lng={}&acc=30.0&time={}&provider=fake".format(lat,lng,int(t))
        vcommon.perr(url)
        urllib.request.urlopen(url).read()
        time.sleep(arg_call_time_ms/1000.)
