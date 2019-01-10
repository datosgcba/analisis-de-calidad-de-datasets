from argparse import ArgumentParser
from src.download import download
from src.cleaner import cleaner
from src.upload import upload
from os import path
import json

parser = ArgumentParser()
parser.add_argument('--no-download', action='store_false', dest='download')
parser.add_argument('--no-data-cleaner', action='store_false', dest='data_cleaner')
parser.add_argument('--no-upload', action='store_false', dest='upload')
routines = parser.parse_args()

script_path = path.abspath(path.dirname(__file__))
manifest_path = path.join(script_path, 'manifest.json')
routine_arguments = {
    'download_datasets_folder': path.join(script_path, 'downloaded-datasets'),
    'clean_datasets_folder': path.join(script_path, 'clean-datasets')
}
with open(manifest_path, 'r') as manifest_file:
    routine_arguments['manifest'] = json.load(manifest_file)


if routines.download:
    download(**routine_arguments)

if routines.data_cleaner:
    cleaner(**routine_arguments)

if routines.upload:
    upload(**routine_arguments)
