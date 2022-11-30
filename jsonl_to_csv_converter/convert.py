#!/usr/bin/env python3
from os import listdir
from os.path import isfile

import json
import csv
# import unicodecsv as csv
data_path = "data/"
output_data_path = "jsonl_to_csv_converter/output_csv/"
supported_extension = ".jsonl"
output_extension = ".csv"
data_files = [file_name for file_name in listdir(data_path) if isfile(data_path + file_name)]

data_jsonl = [file_name for file_name in data_files if file_name.endswith(supported_extension)]

# counter = 0
for file in data_jsonl:
    with open(data_path + file, "r") as jsonl_file:
        json_list = list(jsonl_file)
        
        

    new_file_name = file[:-len(supported_extension)] + output_extension 
    output_data_file = open(output_data_path + new_file_name, "w", newline='', encoding='utf-8-sig')
    csv_writer = csv.writer(output_data_file, dialect='excel', delimiter=';')

    row_counter = 0
# TODO fix correct headers
    for json_entry in json_list:
        row = json.loads(json_entry)
        # write header
        if row_counter == 0:
            csv_writer.writerow(row.keys())
        # write row
        csv_writer.writerow(row.values())
        row_counter += 1
    output_data_file.close()
