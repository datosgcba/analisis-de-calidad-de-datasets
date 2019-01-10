from src.download import download
from src.cleaner import cleaner
from src.upload import upload
from os import path
import json
from src.helpers import argument_parser, Logger

logger = Logger()
script_path = path.abspath(path.dirname(__file__))
manifest_path = path.join(script_path, 'manifest.json')
routine_arguments = {
    'download_datasets_folder': path.join(script_path, 'downloaded-datasets'),
    'clean_datasets_folder': path.join(script_path, 'clean-datasets'),
    'logger': logger
}
with open(manifest_path, 'r') as manifest_file:
    routine_arguments['manifest'] = json.load(manifest_file)
logger.info('Script started with %d datasets in the manifest' % len(routine_arguments['manifest']))

routines = argument_parser()
if routines.download:
    download(**routine_arguments)
else:
    logger.info('Skipping downloader')

if routines.data_cleaner:
    cleaner(**routine_arguments)
else:
    logger.info('Skipping data-cleaner')

if routines.upload:
    upload(**routine_arguments)
else:
    logger.info('Started upload')
