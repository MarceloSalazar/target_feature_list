# Simple script to generate a list of targets and features

# Workflow
# 1. Read from targets.json
# 2. Create dict targets and features
# 3. Print list: screen, txt or csv

import requests
import os
import glob
import pathlib
import urllib, json
import datetime
import time
import subprocess
from datetime import datetime
from argparse import ArgumentParser
from prettytable import PrettyTable

data = []

def read_targets_json():
    global data
    
    file_name = "../mbed-os/targets/targets.json"  
    with open(file_name) as json_file:
        data = json.load(json_file) 

def is_public(target):    
    if 'public' in data[target] and data[target]['public'] == False:
        return False
    else:
        return True

# get features and returns dict
# { feature1='y', feature3='y', ...}
def get_features(target):

    features = dict()

    if 'inherits' in data[target]:
        sub_target = data[target]['inherits']
        for i in sub_target:
            features.update(get_features(i))

    if 'device_has' in data[target]:
        for x in data[target]['device_has']:
            new_dict = dict()
            new_dict[x]='y'
            features.update(new_dict)
           
    return(features)
            
def get_targets_data():
    # Read targets from targets.json and returns dict with features

    targets = dict()
    for i in data:
        if is_public(i) == False:
            continue
        
        features = get_features(i)  
        targets[i]=features
 
    return(targets)

def print_table(target_list):

    # get list of features
    all_features = []
    for i in target_list:
        features = target_list[i].keys()
        for x in features:
            if x not in all_features:
               all_features.append(x)
               
    table_header = ["Target"] + all_features
    table = PrettyTable(table_header)

    table.align['Target'] = 'l'

    for i in target_list:
        temp_features=[]
        for x in all_features:
            if x in target_list[i].keys():
                temp_features.append('y')
            else:
                temp_features.append(' ')
        
        row = [i] + temp_features
        table.add_row(row)

    print(table)
    
    
def main():
    global args

    # Parser handling
    parser = ArgumentParser(description="Script to get list of targets/features")

    parser.add_argument(
        '-m', '--target', dest='target',
        help='Target name', required=False)

    args = parser.parse_args()
   
    read_targets_json()
    target_list = get_targets_data()
    print_table(target_list)

    exit(0)

if __name__ == "__main__":
    main()