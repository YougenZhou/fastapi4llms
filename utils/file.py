import json
import pandas as pd


def read_json(data_path):
    with open(data_path, 'r', encoding='utf-8') as data_file:
        raw_data = json.load(data_file)
        data_file.close()
    return raw_data


def read_csv(data_path):
    return pd.read_csv(data_path)


def save_csv(csv, data_path):
    csv.to_csv(data_path)
