"""
Back Up Files Script
Author: Mike Tung <miketung2013@gmail.com>
2/22/2018
"""

import json
import os
import subprocess as sp
import logging
import datetime


def init_logger(logger_name) -> logging.getLogger():
    """
    Initializes logger object for backup script.

    Args:
        logger_name: name to identify logger.

    Returns:
        logger instance with corresponding name.
    """
    today = datetime.datetime.now().strftime('[%m-%d-%Y]')
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        '[%(levelname)s]\t-\t[%(asctime)s]\t-\t%(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('{}-backup.py.log'.format(today))
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    run_state = os.environ.get('RUN_STATE', 'DEV')

    if run_state == 'DEV':
        logger.setLevel(logging.DEBUG)
    elif run_state == 'PROD':
        logger.setLevel(logging.INFO)
    return logger


log = init_logger('backup.py')


def load_settings() -> dict:
    """
    Loads backup directory, destination directory and other settings for backup
    operation from a json file directed by an environment variable.

    Returns:
        dictionary object containing the configurations.
    """
    backup_config = os.environ.get('BACKUP_CONFIG', None)
    log.info('Loading backup configuration file...')
    if not backup_config:
        log.error('No backup configuration file found!')
        raise AttributeError('Please supply json config file for backup!')

    with open(backup_config) as b:
        settings = json.load(b)

    log.info('Successfully loaded backup configurations!')
    return settings


def issue_rsync(src_dir: str, dest_dir: str) -> None:
    log.info(
        'Backing up source directory {} to server {}'.format(src_dir, dest_dir)
    )
    process = sp.run(
        ['rsync', '-azv', '--delete', src_dir, dest_dir],
        stdout=sp.PIPE,
        stderr=sp.PIPE
    )
    log.info(process.stdout.decode('utf-8'))

    if process.stderr:
        log.error(process.stderr.decode('utf-8'))


def main():
    log.info('Initialized logging!')
    log.info('Loading settings...')
    settings = load_settings()
    log.info('Done loading settings!')
    home_directory = settings['homeDirectory']
    src_directories = settings['sourceDirectories']
    dest_directory = settings['backupDestination']

    for folder in src_directories:
        src = '{}/{}'.format(home_directory, folder)
        issue_rsync(src, dest_directory)


if __name__ == '__main__':
    main()
