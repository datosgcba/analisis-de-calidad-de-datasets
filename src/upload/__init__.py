from os import walk, path


def upload(clean_datasets_folder, connect_ftp, logger, **kwargs):
    logger.info(logger.green('Started upload'))
    ftp = connect_ftp()

    target_folder_name = 'clean-datasets'
    if target_folder_name in ftp.nlst():
        raise Exception('Delete not implemented')
    ftp.mkd(target_folder_name)
    ftp.cwd(target_folder_name)

    for root, dirs, files in walk(clean_datasets_folder):
        if len(root.replace(clean_datasets_folder, '')) == 0:
            continue
        if '/' in root.replace(clean_datasets_folder + '/', ''):
            raise Exception('Unhandled nested folder')

        dataset_folder_name = path.split(root)[1]
        logger.info("Uploading files of " + logger.green(dataset_folder_name))
        ftp.mkd(dataset_folder_name)
        ftp.cwd(dataset_folder_name)

        for filename in files:
            logger.info("Uploading %s/%s" %(dataset_folder_name, filename))
            file_path = path.join(root, filename)
            with open(file_path, 'r') as dataset_file:
                ftp.storlines("STOR " + filename, dataset_file)

        ftp.cwd('..')

    logger.info(logger.green('Upload finished'))
    ftp.quit()
