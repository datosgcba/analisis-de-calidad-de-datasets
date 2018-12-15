import scrapy
from scrapy.http import Request
import json
import os
from scrapy.http import FormRequest

dirname = os.path.dirname(__file__)
manifest_path = os.path.join(dirname, 'manifest.json')
with open(manifest_path, 'r') as f:
    manifest = json.load(f)


def scoped_lambda(func, param):
    return lambda x: func(x, param)


class DatasetsSpider(scrapy.Spider):
    name = 'datasetsspider'

    def start_requests(self):
        return [FormRequest("https://data.buenosaires.gob.ar/api/clients/tokens",
                            formdata={'consumer': 'frontend', 'consumerId': "7fb5addf-5263-4a28-91dd-8f9bbc44ab16"},
                            callback=self.query_datasets)]

    def query_datasets(self, response):
        authorizaton_bearer = json.loads(response.body)['data']
        for dataset in manifest:
            if dataset['slug']:
                slug = dataset['slug']
                url = 'https://data.buenosaires.gob.ar/api/datasets?fields=id&slug=%s' % slug
                yield Request(
                    url=url,
                    callback=scoped_lambda(self.get_download_url, slug),
                    headers={'Authorization': 'Bearer %s' % authorizaton_bearer}
                )

    def get_download_url(self, response, slug):
        response_data = json.loads(response.body)['data']
        if len(response_data) == 0:
            return
        dataset_id = response_data[0]['id']
        url = 'https://data.buenosaires.gob.ar/api/datasets/%s/download' % dataset_id
        yield Request(
            url=url,
            callback=scoped_lambda(self.save_file, slug),
        )

    def save_file(self, response, slug):
        file_path = os.path.join(dirname, '%s.zip' % slug)
        self.logger.info('Saving file to %s', file_path)
        with open(file_path, 'wb') as new_dataset_file:
            new_dataset_file.write(response.body)
