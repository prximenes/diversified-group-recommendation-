#!/usr/bin/env python3

import pandas as pd
import numpy as np
import csv
import os

def add_hotel_info(filename):
    datContent = [i.strip().split() for i in open(filename).readlines()]
    hotel_id = filename.split('_')[1].split('.')[0]
    for item in datContent:
        if item != []:
            if '<Overall' in item[0]:
                if len(item) == 1:
                    ratings.append(item[0].split('>')[1])
                #stuff.append(item[1].split('>')[1])
                #print(item)
            if 'Author' in item[0]:
                users.append(item[0].split('>')[1])
                hotels.append(hotel_id)



def get_list_from_csv(fp):
    l = list()
    with open(fp,'r') as fil:
        in_reader = csv.reader(fil,delimiter=",")
        for row in in_reader:
            l.append(row)
    return l 
    

users = []
hotels = []
ratings = []
root = os.getcwd()
for filename in os.listdir(root):
    if '.dat' in filename:
        add_hotel_info(filename)
        
df = pd.DataFrame()
df['user_id'] = pd.Series(users)
df['item_id'] = pd.Series(hotels)
df['score'] = pd.Series(ratings)

target_dir = '../parsed-databases/'
csv_name = 'trip_advisor.csv'
if not os.path.exists(target_dir):
    os.mkdir(target_dir)


df.to_csv(csv_name)


ls = get_list_from_csv(csv_name)
ls.pop(0)

with open(target_dir+csv_name, "w") as out_csv:
    out_writer = csv.writer(out_csv)
    for row in ls:
        parsed_row = row[1:]
        out_writer.writerow(parsed_row)
