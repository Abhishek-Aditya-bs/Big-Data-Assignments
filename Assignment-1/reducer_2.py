#! /usr/bin/env python3

import sys

def reduce_mapper():
    current_state = ""
    current_city = ""
    count = 0
    total_count = 0
    for line in sys.stdin:
        state,city,_ = line.strip().split(",")
        if current_state == "":
            print(state)
            current_state = state
            current_city = city
            count = 1
            total_count = 1
            continue

        if state != current_state:
            print(current_city,count)
            print(current_state,total_count)
            current_state = state
            print(current_state)
            current_city = city
            count = 1
            total_count = 1
            continue

        else:
            total_count += 1
            if city != current_city:
                print(current_city,count)
                current_city = city
                count = 1
            else:
                count += 1
    print(current_city,count)
    print(current_state,total_count)
            
        

if __name__ == "__main__":
    reduce_mapper()
