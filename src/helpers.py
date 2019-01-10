from argparse import ArgumentParser
import logging


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument('--no-download', action='store_false', dest='download')
    parser.add_argument('--no-data-cleaner', action='store_false', dest='data_cleaner')
    parser.add_argument('--no-upload', action='store_false', dest='upload')
    return parser.parse_args()


class Logger:
    RESET_SEQ = "\033[0m"

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
        self.logger = logging.getLogger()

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    @classmethod
    def green(cls, message):
        return "\033[1;32m" + message + cls.RESET_SEQ

    @classmethod
    def red(cls, message):
        return "\033[1;31m" + message + cls.RESET_SEQ
