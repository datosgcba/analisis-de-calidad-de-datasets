# coding=utf-8
from data_cleaner import DataCleaner
from os import path, makedirs
import json


def cleaner(**kwargs):
    script_path = path.dirname(__file__)

    for dataset in kwargs['manifest']:
        dataset_rules_path = path.join(script_path, 'rules', '%s.json' % dataset)
        if not path.exists(dataset_rules_path):
            continue

        with open(dataset_rules_path, 'r') as json_rules:
            dataset_rules = json.load(json_rules)

        for dataset_file_rules in dataset_rules:
            csv_input = path.join(kwargs['download_datasets_folder'], dataset, dataset_file_rules['file'])
            if not path.exists(csv_input):
                continue

            csv_output = path.join(kwargs['clean_datasets_folder'], dataset, dataset_file_rules['file'])

            if not path.exists(kwargs['clean_datasets_folder']):
                makedirs(kwargs['clean_datasets_folder'])

            clean_dataset_folder = path.join(kwargs['clean_datasets_folder'], dataset)
            if not path.exists(clean_dataset_folder):
                makedirs(clean_dataset_folder)

            parse_options = dataset_file_rules.get('parse_options', {})
            dc = DataCleaner(csv_input, **parse_options)
            dc.clean(dataset_file_rules['data-cleaner-rules'])
            dc.df.set_index(dc.df.columns[0]).to_csv(
                csv_output,
                encoding=dc.OUTPUT_ENCODING,
                sep=dc.OUTPUT_SEPARATOR,
                quotechar=dc.OUTPUT_QUOTECHAR
            )
