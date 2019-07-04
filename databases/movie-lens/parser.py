#!/usr/bin/env python3

import csv

database= "u.data"
csv_file = "../parsed-databases/movie-lenz.csv"

with open(database, "r") as db:
    in_reader = csv.reader(db, delimiter = '\t')
    with open(csv_file, "w") as out_csv:
        out_writer = csv.writer(out_csv)
        for row in in_reader:
            parsed_row = row[:-1]
            out_writer.writerow(parsed_row)
