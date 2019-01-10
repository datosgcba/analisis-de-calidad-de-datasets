import logging
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess
from dataset_spider import DatasetSpider


def download(**kwargs):
    configure_logging(install_root_handler=False)
    logging.basicConfig(level=logging.WARNING)
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(DatasetSpider, **kwargs)
    process.start()
