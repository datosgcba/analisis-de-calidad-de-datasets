from ftplib import FTP


def download_from_ftp(**kwars):
    ftp = FTP('ftp.buenosaires.gob.ar')
    ftp.login('datosabiertos', kwars['password'])
    ftp.cwd('datasets')
    ftp.retrlines('LIST')

