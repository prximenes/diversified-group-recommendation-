#!/usr/bin/env python3

import csv
import re 
import numpy as np
import pandas as pd
from functools import reduce
import os 

database = 'amazon_mp3'
base_dir = '../parsed-databases/'
filename = 'amazon.csv'

pattern = re.compile('#####*')
ll = []
l = []
with open(database,'r') as db:
    reader = csv.reader(db)
    for row in reader:
        if len(row) == 0:
            continue
        elif pattern.match(row[0]):
            ll.append(l)
            l = []
        else:
            if len(row) == 1:
                l.append(row[0])
            else:
                l.append(reduce((lambda x,y: x+y),row))

dicts = []
for i in range(len(ll)):
    cols = list(map((lambda x: x.split(':')[0].split(']')[0].split('[')[1]),ll[i]))
    vals = list(map((lambda x: x.split(']:')[1]),ll[i]))
    dic = dict(zip(cols, vals))
    dicts.append(dic)
    
dicts = dicts[1:]

ls = list()

for row in dicts:    
    ls.append([row.get("id"),row.get("productId"),row.get('rating')])


if not os.path.exists(base_dir):
    os.mkdir(base_dir)


with open(base_dir+filename, "w") as out_csv:
    out_writer = csv.writer(out_csv)
    for row in ls:
        out_writer.writerow(row)
