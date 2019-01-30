from argparse import ArgumentParser
import logging
import json
from ftplib import FTP
from os import path


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument('--no-download', action='store_false', dest='download')
    parser.add_argument('--no-data-cleaner', action='store_false', dest='data_cleaner')
    parser.add_argument('--no-upload', action='store_false', dest='upload')
    parser.add_argument('--download-via-scrapy', action='store_true', dest='download_scrapy')
    return parser.parse_args()


def load_json(filepath):
    with open(filepath, 'r') as manifest_file:
        return json.load(manifest_file)


def connect_ftp():
    script_path = path.dirname(__file__)
    password_file_path = path.join(script_path, 'ftp_password')
    if not path.exists(password_file_path):
        raise Exception('Missing ftp_password file')
    with open(password_file_path, 'r') as password_file:
        ftp_password = password_file.read().strip()
    ftp = FTP('ftp.buenosaires.gob.ar')
    ftp.login('datosabiertos', ftp_password)
    return ftp


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
