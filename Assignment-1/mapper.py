#!/usr/bin/env python3

import sys
import json
import math
from datetime import datetime

def get_input():
    for line in sys.stdin:
        yield json.loads(line)

if __name__ == "__main__":
    for data in get_input():
        flag = 0
        for values in [data["Severity"],data["Visibility(mi)"],data["Precipitation(in)"],data["Sunrise_Sunset"],data["Weather_Condition"],data["Description"]]:
            if type(values) == float and math.isnan(values):
                flag = 1
                break
        if flag:
            continue
        
        if data["Severity"] >= 2 and data["Visibility(mi)"] <= 10.0 and data["Precipitation(in)"] >= 0.2 and data["Sunrise_Sunset"] == "Night":
            flag = 0
            for weather in ["Heavy Snow", "Thunderstorm", "Heavy Rain", "Heavy Rain Showers", "Blowing Dust"]:
                if weather.lower() == data["Weather_Condition"].lower():
                    flag = 1
                    break
            if flag:
                for desc in ["lane blocked", "shoulder blocked", "overturned vehicle"]:
                    if desc in data["Description"].lower():
                        date_time = data["Start_Time"].split()
                        date_time[1] = date_time[1][:8]
                        time = datetime.strptime(" ".join(date_time),"%Y-%m-%d %H:%M:%S")
                        print(f"{time.hour},1")
                        break
            else: continue