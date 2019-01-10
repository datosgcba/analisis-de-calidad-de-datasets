import logging
from scrapy.crawler import CrawlerProcess
from dataset_spider import DatasetSpider


def disable_scrapy_loggers():
    loggers = [
        'scrapy.core.engine', 'scrapy.extensions.logstats', 'scrapy.core.downloader.handlers.http11',
        'scrapy.crawler', 'scrapy.middleware', 'scrapy.extensions.telnet', 'scrapy.statscollectors',
        'scrapy.utils.log'
    ]
    for logger_name in loggers:
        logging.getLogger(logger_name).disabled = True


def download(**kwargs):
    disable_scrapy_loggers()
    process = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
        install_root_handler=False
    )
    process.crawl(DatasetSpider, **kwargs)
    process.start()
