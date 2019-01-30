from os import path, makedirs


def download_dataset_files(ftp, target_folder):
    dataset_files = ftp.nlst()
    for dataset_file in dataset_files:
        target_file_path = path.join(target_folder, dataset_file)
        target_file = open(target_file_path, 'wb')
        ftp.retrbinary('RETR ' + dataset_file, target_file.write)


def download_from_ftp(manifest, logger, download_datasets_folder, connect_ftp, **kwargs):
    ftp = connect_ftp()
    ftp.cwd('datasets')
    available_datasets = ftp.nlst()

    for dataset in manifest:
        target_dataset_folder = path.join(download_datasets_folder, dataset)
        if path.exists(target_dataset_folder):
            logger.info("Skipping download of %s" % dataset)
            continue

        if dataset not in available_datasets:
            logger.info("Missing ftp dataset folder " + logger.red(dataset))
            continue
        logger.info("Found ftp dataset folder " + logger.green(dataset) + ". Downloading files")

        makedirs(target_dataset_folder)
        ftp.cwd(dataset)
        download_dataset_files(ftp, target_dataset_folder)
        ftp.cwd('..')

    ftp.quit()
