# -*- coding: utf-8 -*

import json
import csv
import pandas as pd

notices_path = "../../dataset/notices.csv"
notices_type_path = "../../out/dataset_statistics/notice_type.csv"
notices_type_count_path = "../../out/dataset_statistics/notice_type_count.csv"

notice_type_head = ['notice_id','notice_type']
notices_type_count_head  =['notice_type','count']

def create_csv(path, csv_head):
    with open(path, 'wb') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(csv_head)


def write_csv(path, data_row):
    with open(path, 'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)

create_csv(notices_type_path, notice_type_head)
notices = pd.read_csv(notices_path)
print notices
for j in range(len(notices)):
    notice_id = notices['notice_id'].iloc[j]
    notice_type = notices['notice_type'].iloc[j].encode('utf-8')
    new_row = [notice_id,notice_type]
    write_csv(notices_type_path, new_row)

create_csv(notices_type_count_path, notices_type_count_path)
notice_df = pd.read_csv(notices_type_path)
grouped_notices = notice_df.groupby('notice_type')
for index, data in grouped_notices:
    notice_type = index
    notice_count = len(data)
    new_row = [notice_type, notice_count]
    write_csv(notices_type_count_path,new_row)



