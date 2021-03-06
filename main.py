from src.download import download
from src.cleaner import cleaner
from src.upload import upload
from os import path
from src.helpers import argument_parser, Logger, load_json, connect_ftp

logger = Logger()
script_path = path.abspath(path.dirname(__file__))
arguments = argument_parser()
routine_arguments = {
    'download_datasets_folder': path.join(script_path, 'downloaded-datasets'),
    'clean_datasets_folder': path.join(script_path, 'clean-datasets'),
    'logger': logger,
    'manifest': load_json(path.join(script_path, 'manifest.json')),
    'download_scrapy': arguments.download_scrapy,
    'connect_ftp': connect_ftp,
}
logger.info('Script started with %d datasets in the manifest' % len(routine_arguments['manifest']))

if arguments.download:
    download(**routine_arguments)
else:
    logger.info('Skipping downloader')

if arguments.data_cleaner:
    cleaner(**routine_arguments)
else:
    logger.info('Skipping data-cleaner')

if arguments.upload:
    upload(**routine_arguments)
else:
    logger.info('Skipping upload')
