from data_cleaner import DataCleaner
import os


def clean_and_save(input_path, output_path):
    output_folder = os.path.join(os.path.dirname(output_path))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dc = DataCleaner(input_path)
    dc.clean(rules)
    dc.df.set_index(dc.df.columns[0]).to_csv(
        output_path,
        encoding=dc.OUTPUT_ENCODING,
        sep=dc.OUTPUT_SEPARATOR,
        quotechar=dc.OUTPUT_QUOTECHAR
    )


if __name__ == '__main__':
    root_datasets_folder = os.path.dirname(__file__)
    csv_input = os.path.join(root_datasets_folder, "obras-registradas", "obras-registradas.csv")
    csv_output = os.path.join(root_datasets_folder, "obras-registradas", "clean", "obras-registradas.csv")
    rules = []
    clean_and_save(csv_input, csv_output)
