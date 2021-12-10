#!/usr/bin/env python3

import sys

def reduce_mapper():
    hour_dictionary = {str(hr):0 for hr in range(0,24)}
    for line in sys.stdin:
        hr,_ = line.strip().split(",")
        hour_dictionary[hr] += 1
    for key in hour_dictionary:
        if hour_dictionary[key] == 0:
            continue
        print(f"{int(key)} {hour_dictionary[key]}")

if __name__ == "__main__":
    reduce_mapper()