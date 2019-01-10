# coding=utf-8
import json
import scrapy
from scrapy.http import Request
from scrapy.http import FormRequest
import zipfile
from os import path, remove, makedirs


class DatasetSpider(scrapy.Spider):
    name = 'datasetspider'
    authorizaton_bearer = ''

    def __init__(self, *args, **kwargs):
        self.manifest = [dataset for dataset in kwargs['manifest']]
        self.download_datasets_folder = kwargs['download_datasets_folder']
        self.log = kwargs['logger']
        super(DatasetSpider, self).__init__(*args, **kwargs)

    def next_dataset(self):
        while len(self.manifest) != 0:
            candidate_dataset = self.manifest.pop()
            dataset_folder = path.join(self.download_datasets_folder, candidate_dataset)
            if not path.exists(dataset_folder):
                return candidate_dataset
        return None

    @staticmethod
    def scoped_lambda(func, param):
        return lambda x: func(x, param)

    def start_requests(self):
        self.log.info('Requesting authorization from server')
        return [FormRequest("https://data.buenosaires.gob.ar/api/clients/tokens",
                            formdata={'consumer': 'frontend', 'consumerId': "7fb5addf-5263-4a28-91dd-8f9bbc44ab16"},
                            callback=self.save_authorizaton_bearer)]

    def save_authorizaton_bearer(self, response):
        self.authorizaton_bearer = json.loads(response.body)['data']
        self.log.info('Got authorization from server ' + self.log.green('✓'))
        self.log.info('Starting to query the datasets')
        return self.query_next_dataset()

    def query_next_dataset(self):
        dataset = self.next_dataset()
        if dataset is None:
            return
        self.log.info('Querying dataset %s' % self.log.green(dataset))
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
        self.log.info(
            'Got id %s for %s. Downloading zip file...' % (self.log.green(dataset_id), self.log.green(dataset)))
        url = 'https://data.buenosaires.gob.ar/api/datasets/%s/download' % dataset_id
        yield Request(
            url=url,
            callback=self.scoped_lambda(self.save_file, dataset),
        )

    def save_file(self, response, dataset):
        file_path = path.join(self.download_datasets_folder, '%s.zip' % dataset)
        self.log.info('Saving %s.zip' % dataset)
        if not path.exists(self.download_datasets_folder):
            makedirs(self.download_datasets_folder)
        with open(file_path, 'wb') as new_dataset_file:
            new_dataset_file.write(response.body)
            self.log.info('Unzipping dataset...')
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.download_datasets_folder)
                self.log.info('Unzipped! Removing the zip file')
                remove(file_path)
        except zipfile.BadZipfile:
            self.log.error('Unable to unzip file %s.zip %s' % (dataset, self.log.red('BAD ZIPFILE')))
        return self.query_next_dataset()
