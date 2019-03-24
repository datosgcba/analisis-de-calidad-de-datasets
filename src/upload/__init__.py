from os import walk, path


def move_into_target_folder(ftp):
    target_folder_name = 'clean-datasets'
    if target_folder_name not in ftp.nlst():
        ftp.mkd(target_folder_name)
    ftp.cwd(target_folder_name)


def move_into_dataset_folder(ftp, dataset_folder_name, logger):
    dataset_folder_already_exists = dataset_folder_name in ftp.nlst()
    if not dataset_folder_already_exists:
        ftp.mkd(dataset_folder_name)
    ftp.cwd(dataset_folder_name)
    if dataset_folder_name:
        logger.info('Folder for %s already existed. Removing files in it' % dataset_folder_name)
        clean_current_folder(ftp)


def clean_current_folder(ftp):
    names = ftp.nlst()
    for name in names:
        if path.split(name)[1] in ('.', '..'):
            continue
        ftp.delete(name)
    return


def upload(clean_datasets_folder, connect_ftp, logger, **kwargs):
    logger.info(logger.green('Started upload'))
    ftp = connect_ftp()
    move_into_target_folder(ftp)

    for root, dirs, files in walk(clean_datasets_folder):
        if root == clean_datasets_folder:
            continue
        if '/' in root.replace(clean_datasets_folder + '/', ''):
            raise Exception('Unhandled nested folder')

        dataset_folder_name = path.split(root)[1]
        logger.info("Uploading files of " + logger.green(dataset_folder_name))
        move_into_dataset_folder(ftp, dataset_folder_name, logger)

        for filename in files:
            logger.info("Uploading %s/%s" %(dataset_folder_name, filename))
            file_path = path.join(root, filename)
            with open(file_path, 'rb') as dataset_file:
                ftp.storbinary("STOR " + filename, dataset_file)

        ftp.cwd('..')

    logger.info(logger.green('Upload finished'))
    ftp.quit()
