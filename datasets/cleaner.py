from data_cleaner import DataCleaner
from os import path, makedirs
from cleaner_rules import target_datasets


def makedir_if_doesnt_exist(output_path):
    output_folder = path.join(path.dirname(output_path))
    if not path.exists(output_folder):
        makedirs(output_folder)


if __name__ == '__main__':
    root_datasets_folder = path.dirname(__file__)

    for dataset in target_datasets:
        csv_input = path.join(root_datasets_folder, dataset['input_path'])
        csv_output = path.join(root_datasets_folder, dataset['output_path'])
        dataset_rules = dataset['cleaner_rules']
        parse_options = dataset.get('parse_options', {})

        makedir_if_doesnt_exist(csv_output)

        dc = DataCleaner(csv_input, **parse_options)
        dc.clean(dataset_rules)
        dc.df.set_index(dc.df.columns[0]).to_csv(
            csv_output,
            encoding=dc.OUTPUT_ENCODING,
            sep=dc.OUTPUT_SEPARATOR,
            quotechar=dc.OUTPUT_QUOTECHAR
        )
