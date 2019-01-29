import logging
from scrapy.crawler import CrawlerProcess
from dataset_spider import DatasetSpider
from ftp import download_from_ftp
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


def download_via_ftp(**kwargs):
    logger = kwargs['logger']
    logger.info(logger.green('Started ftp downloader'))
    download_from_ftp(**kwargs)
    return


def download_via_scrapy(**kwargs):
    logger = kwargs['logger']
    logger.info(logger.green('Started scrapy downloader'))
    disable_scrapy_loggers()
    process = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
        install_root_handler=False
    )
    process.crawl(DatasetSpider, **kwargs)
    process.start()


def download(**kwargs):
    logger = kwargs['logger']
    if not have_dataset_to_download(**kwargs):
        logger.info('All datasets already downloaded. Skipping download routine')
        return

    if kwargs['download_scrapy']:
        download_via_scrapy(**kwargs)
    else:
        download_via_ftp(**kwargs)
