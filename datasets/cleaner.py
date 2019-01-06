from data_cleaner import DataCleaner
from os import path, makedirs
from cleaner_rules import cleaner_rules


def clean_and_save(input_path, output_path, rules):
    output_folder = path.join(path.dirname(output_path))
    if not path.exists(output_folder):
        makedirs(output_folder)

    dc = DataCleaner(input_path)
    dc.clean(rules)
    dc.df.set_index(dc.df.columns[0]).to_csv(
        output_path,
        encoding=dc.OUTPUT_ENCODING,
        sep=dc.OUTPUT_SEPARATOR,
        quotechar=dc.OUTPUT_QUOTECHAR
    )


def make_dataset_path(*paths):
    return path.join(root_datasets_folder, *paths)


def clean_dataset_path(original_dataset_path):
    dirname, filename = path.split(original_dataset_path)
    return path.join(dirname, 'clean', filename)


def rules_for_dataset(dataset_path):
    dataset_folder_path, dataset_filename = path.split(dataset_path)
    dataset_root_folder, dataset_folder_name = path.split(dataset_folder_path)
    dataset_path = path.join(dataset_folder_name, dataset_filename)
    if dataset_path in cleaner_rules:
        return cleaner_rules[dataset_path]
    dirname = path.dirname(dataset_path)
    if dirname in cleaner_rules:
        return cleaner_rules[dirname]
    raise Exception("No rules found for %s" % dataset_path)


if __name__ == '__main__':
    root_datasets_folder = path.dirname(__file__)

    target_datasets = [
        make_dataset_path("obras-registradas", "obras-registradas.csv")
    ]

    for csv_input in target_datasets:
        csv_output = clean_dataset_path(csv_input)
        rules = rules_for_dataset(csv_input)
        clean_and_save(csv_input, csv_output, rules)
