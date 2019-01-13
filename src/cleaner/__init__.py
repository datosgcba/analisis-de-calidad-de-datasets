# coding=utf-8
from data_cleaner import DataCleaner
from os import path, makedirs
import json
import warnings
from time import time

script_path = path.dirname(__file__)


def load_rules_for_dataset(dataset, logger):
    dataset_rules_path = path.join(script_path, 'rules', '%s.json' % dataset)
    if not path.exists(dataset_rules_path):
        logger.info('No data-cleaner rules found for dataset %s' % logger.red(dataset))
        return None
    with open(dataset_rules_path, 'r') as json_rules:
        return json.load(json_rules)


def apply_rules_to_dataset(csv_input, csv_output, dataset_file_rules, parse_options):
    for key in parse_options:
        parse_options[key] = parse_options[key].encode('ascii')

    with warnings.catch_warnings(record=True) as catched_warnings:
        dc = DataCleaner(csv_input, **parse_options)
        dc.clean(dataset_file_rules['data-cleaner-rules'])
        dc.df.set_index(dc.df.columns[0]).to_csv(
            csv_output,
            encoding=dc.OUTPUT_ENCODING,
            sep=dc.OUTPUT_SEPARATOR,
            quotechar=dc.OUTPUT_QUOTECHAR
        )
        return catched_warnings


def create_folder_if_does_not_exists(folder_path):
    if not path.exists(folder_path):
        makedirs(folder_path)


def collect_warnings(datacleaner_warnings, dataset, dataset_file):
    if len(datacleaner_warnings) == 0:
        return []
    dataset_divide = "###################################\n"
    dataset_info = "%s %s\n" % (dataset, dataset_file)
    warning_messages = [
                           warning.message.message.replace("\n", " ") + "\n"
                           for warning in datacleaner_warnings
                       ] + ["\n\n"]
    return [dataset_divide, dataset_info] + warning_messages


def save_warnings(routine_warnings, logger):
    if len(routine_warnings) > 0:
        warnings_filename = "warnings_%d.log" % time()
        logger.info("Warnings de datacleaner escritas en el archivo %s" % logger.red(warnings_filename))
        with open(warnings_filename, 'w') as warnings_file:
            warnings_file.writelines(routine_warnings)


def cleaner(manifest, logger, clean_datasets_folder, download_datasets_folder):
    logger.info(logger.green('Started data-cleaner'))
    create_folder_if_does_not_exists(clean_datasets_folder)

    routine_warnings = []
    for dataset in manifest:
        dataset_rules = load_rules_for_dataset(dataset, logger)
        if dataset_rules is None:
            continue

        for dataset_file_rules in dataset_rules:
            dataset_file = dataset_file_rules['file']
            csv_input = path.join(download_datasets_folder, dataset, dataset_file)
            if not path.exists(csv_input):
                logger.info('Skipping missing file %s' % logger.red(dataset_file))
                continue

            output_dataset_folder = path.join(clean_datasets_folder, dataset)
            create_folder_if_does_not_exists(output_dataset_folder)
            csv_output = path.join(output_dataset_folder, dataset_file)

            logger.info('Applying rules for file %s' % logger.green(dataset_file))
            parse_options = dataset_file_rules.get('parse_options', {})
            datacleaner_warnings = apply_rules_to_dataset(csv_input, csv_output, dataset_file_rules, parse_options)
            routine_warnings += collect_warnings(datacleaner_warnings, dataset, dataset_file)
    save_warnings(routine_warnings, logger)
