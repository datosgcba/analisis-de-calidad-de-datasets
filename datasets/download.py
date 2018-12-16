import scrapy
from scrapy.http import Request
import json
import os
from scrapy.http import FormRequest
import zipfile

root_datasets_folder = os.path.dirname(__file__)


class DatasetIterator:
    manifest_path = os.path.join(root_datasets_folder, 'manifest.json')
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    @classmethod
    def next_dataset(cls):
        while len(cls.manifest) != 0:
            candidate_dataset = cls.manifest.pop()
            slug = candidate_dataset['slug']
            dataset_folder = os.path.join(root_datasets_folder, slug)
            if not os.path.exists(dataset_folder):
                return candidate_dataset
        return None


class DatasetsSpider(scrapy.Spider):
    name = 'datasetsspider'
    authorizaton_bearer = ''

    @staticmethod
    def scoped_lambda(func, param):
        return lambda x: func(x, param)

    def start_requests(self):
        return [FormRequest("https://data.buenosaires.gob.ar/api/clients/tokens",
                            formdata={'consumer': 'frontend', 'consumerId': "7fb5addf-5263-4a28-91dd-8f9bbc44ab16"},
                            callback=self.save_authorizaton_bearer)]

    def save_authorizaton_bearer(self, response):
        self.authorizaton_bearer = json.loads(response.body)['data']
        return self.query_next_dataset()

    def query_next_dataset(self):
        dataset = DatasetIterator.next_dataset()
        if dataset is None:
            return
        slug = dataset['slug']
        url = 'https://data.buenosaires.gob.ar/api/datasets?fields=id&slug=%s' % slug
        yield Request(
            url=url,
            callback=self.scoped_lambda(self.get_download_url, slug),
            headers={'Authorization': 'Bearer %s' % self.authorizaton_bearer}
        )

    def get_download_url(self, response, slug):
        response_data = json.loads(response.body)['data']
        if len(response_data) == 0:
            return
        dataset_id = response_data[0]['id']
        self.logger.info('Got id %s for %s', dataset_id, slug)
        url = 'https://data.buenosaires.gob.ar/api/datasets/%s/download' % dataset_id
        yield Request(
            url=url,
            callback=self.scoped_lambda(self.save_file, slug),
        )

    def save_file(self, response, slug):
        file_path = os.path.join(root_datasets_folder, '%s.zip' % slug)
        self.logger.info('Saving file to %s', file_path)
        with open(file_path, 'wb') as new_dataset_file:
            new_dataset_file.write(response.body)
        unzip_folder = os.path.join(root_datasets_folder, slug)
        if not os.path.exists(unzip_folder):
            os.makedirs(unzip_folder)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_folder)
        os.remove(file_path)
        return self.query_next_dataset()
