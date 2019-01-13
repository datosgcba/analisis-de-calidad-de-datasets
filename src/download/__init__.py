import logging
from scrapy.crawler import CrawlerProcess
from dataset_spider import DatasetSpider
from os import path


def disable_scrapy_loggers():
    loggers = [
        'scrapy.core.engine', 'scrapy.extensions.logstats', 'scrapy.core.downloader.handlers.http11',
        'scrapy.crawler', 'scrapy.middleware', 'scrapy.extensions.telnet', 'scrapy.statscollectors',
        'scrapy.utils.log'
    ]
    for logger_name in loggers:
        logging.getLogger(logger_name).disabled = True


def have_dataset_to_download(manifest, download_datasets_folder, **kwargs):
    for dataset in manifest:
        dataset_folder = path.join(download_datasets_folder, dataset)
        if not path.exists(dataset_folder):
            return True
    return False


def download(**kwargs):
    logger = kwargs['logger']
    if not have_dataset_to_download(**kwargs):
        logger.info('All datasets already downloaded. Skipping download routine')
        return

    logger.info(logger.green('Started downloader'))
    disable_scrapy_loggers()
    process = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
        install_root_handler=False
    )
    process.crawl(DatasetSpider, **kwargs)
    process.start()
