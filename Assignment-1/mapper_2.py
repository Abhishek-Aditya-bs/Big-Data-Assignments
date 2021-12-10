#! /usr/bin/env python3

from json.decoder import JSONDecoder
import sys
import json
import math
import requests
from datetime import datetime

def get_input():
    for line in sys.stdin:
        yield json.loads(line)

def eucledian(start_point,end_point):
    x1,x2 = start_point[0],end_point[0]
    y1,y2 = start_point[1], end_point[1]
    d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return d

def post(start_point):
    r = requests.post(url = "http://20.185.44.219:5000/", json = {"latitude": start_point[0],"longitude": start_point[1]})
    data = r.json()
    return (data["state"],data["city"]) 



if __name__ == "__main__":
    end_lat, end_lng = float(sys.argv[1]),float(sys.argv[2])
    D = float(sys.argv[3])
    for data in get_input():
        flag = 0
        for values in [float(data["Start_Lat"]),float(data["Start_Lng"])]:#,data["Severity"],data["Visibility(mi)"],data["Precipitation(in)"],data["Sunrise_Sunset"],data["Weather_Condition"],data["Description"]]:
            if type(values) == float and math.isnan(values):
                flag = 1
                break
        if flag:
            continue

        if eucledian((float(data["Start_Lat"]),float(data["Start_Lng"])),(end_lat,end_lng)) > D:
            continue

        state, city = post((float(data["Start_Lat"]),float(data["Start_Lng"])))
        if state ==None or city == None:
            continue
        print(f"{state},{city},1")








        
