import scrapy
from scrapy.http import Request
import json
import os
from scrapy.http import FormRequest
import zipfile
import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    level=logging.WARNING
)

root_datasets_folder = os.path.dirname(__file__)


class DatasetIterator:
    manifest_path = os.path.join(root_datasets_folder, 'manifest.json')
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    @classmethod
    def next_dataset(cls):
        while len(cls.manifest) != 0:
            candidate_dataset = cls.manifest.pop()
            dataset_folder = os.path.join(root_datasets_folder, candidate_dataset)
            if not os.path.exists(dataset_folder):
                return candidate_dataset
        return None


class DatasetsSpider(scrapy.Spider):
    name = 'datasetsspider'
    authorizaton_bearer = ''

    def __init__(self, *args, **kwargs):
        loggers = [
            'scrapy.core.engine', 'scrapy.extensions.logstats', 'scrapy.core.downloader.handlers.http11',
            'scrapy.crawler', 'scrapy.middleware', 'scrapy.extensions.telnet', 'scrapy.statscollectors',
            'scrapy.utils.log'
        ]
        logging.basicConfig(level=logging.INFO)
        for logger_name in loggers:
            logging.getLogger(logger_name).setLevel(logging.ERROR)
        super(DatasetsSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def scoped_lambda(func, param):
        return lambda x: func(x, param)

    def start_requests(self):
        self.logger.info('Starting dataset spider')
        return [FormRequest("https://data.buenosaires.gob.ar/api/clients/tokens",
                            formdata={'consumer': 'frontend', 'consumerId': "7fb5addf-5263-4a28-91dd-8f9bbc44ab16"},
                            callback=self.save_authorizaton_bearer)]

    def save_authorizaton_bearer(self, response):
        self.authorizaton_bearer = json.loads(response.body)['data']
        self.logger.info('Got authorization from server. Starting to query the datasets')
        return self.query_next_dataset()

    def query_next_dataset(self):
        dataset = DatasetIterator.next_dataset()
        if dataset is None:
            self.logger.info('No dataset left. Ending crawler')
            return
        self.logger.info('Querying dataset %s', dataset)
        url = 'https://data.buenosaires.gob.ar/api/datasets?fields=id,slug&slug=%s' % dataset
        yield Request(
            url=url,
            callback=self.scoped_lambda(self.get_download_url, dataset),
            headers={'Authorization': 'Bearer %s' % self.authorizaton_bearer}
        )

    def get_download_url(self, response, dataset):
        response_data = json.loads(response.body)['data']
        if len(response_data) == 0:
            return
        dataset_id = [dataset_data for dataset_data in response_data if dataset_data['slug'] == dataset][0]['id']
        self.logger.info('Got id %s for %s. Downloading zip file...', dataset_id, dataset)
        url = 'https://data.buenosaires.gob.ar/api/datasets/%s/download' % dataset_id
        yield Request(
            url=url,
            callback=self.scoped_lambda(self.save_file, dataset),
        )

    def save_file(self, response, dataset):
        file_path = os.path.join(root_datasets_folder, '%s.zip' % dataset)
        self.logger.info('Saving zip file to %s', file_path)
        with open(file_path, 'wb') as new_dataset_file:
            new_dataset_file.write(response.body)
        self.logger.info('Unzipping dataset...')
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(root_datasets_folder)
                self.logger.info('Unzipped! Removing the zip file')
                os.remove(file_path)
        except zipfile.BadZipfile:
            self.logger.error('Unable to unzip file %s BAD ZIPFILE', file_path)
        return self.query_next_dataset()
