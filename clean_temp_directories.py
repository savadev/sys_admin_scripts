#!/usr/bin/env python3.6
"""
Temporary Directory Cleanup Script
Author: Mike Tung <miketung2013@gmail.com>
2/28/2018
"""

import glob
import json
import os
import subprocess as sp
import logging
import datetime


def init_logger(location: str, logger_name: str) -> logging.getLogger():
    """
    Initializes logger object for backup script.

    Args:
        location: directory to store logs.
        logger_name: name to identify logger.

    Returns:
        logger instance with corresponding name.
    """

    if not location:
        raise AttributeError('No backup directory specified!')


    today = datetime.datetime.now().strftime('[%m-%d-%Y]')
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        '[%(levelname)s]\t-\t[%(asctime)s]\t-\t%(name)s\t%(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('{}/{}-sys_admin.log'.format(location, today))
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    run_state = os.environ.get('RUN_STATE', 'DEV')

    if run_state == 'DEV':
        logger.setLevel(logging.DEBUG)
    elif run_state == 'PROD':
        logger.setLevel(logging.INFO)

    logger.info('Successfully initialized logger!')
    logger.info('Backup Logs Directory: {}'.format(location))
    return logger


log = init_logger(
    os.environ.get('BACKUP_DIR', None), 'clean_temp_directories.py'
)


def load_settings() -> dict:
    """
    Loads configurations from a json file, specified from environment variable.

    Returns:
        dictionary object containing the configurations.
    """
    backup_config = os.environ.get('BACKUP_CONFIG', './settings.json')
    log.info('Loading backup configuration file...')
    if not backup_config:
        log.error('No backup configuration file found!')
        raise AttributeError('Please supply json config file for backup!')

    with open(backup_config) as b:
        settings = json.load(b)

    log.info('Successfully loaded backup configurations!')
    return settings


def issue_delete(target_dir) -> None:
    """
    Issues command to delete files from provided directory.

    Args:
        target_dir: directory whose files should be deleted.

    Returns:
        None
    """
    log.info('deleting files in {}'.format(target_dir))

    for fi in glob.glob('{}/*'.format(target_dir)):
        log.info('deleting {} from {}...'.format(fi, target_dir))
        process = sp.run(['rm', '-rfv', fi], stdout=sp.PIPE, stderr=sp.PIPE)
        log.info(process.stdout.decode('utf-8'))

        if process.stderr:
            log.error(process.stderr.decode('utf-8'))


def main():
    """
    Main function to kick off directory clean up.

    Returns:
        None
    """
    log.info('Initialized logging!')
    log.info('Loading settings...')
    settings = load_settings()
    log.info('Done loading settings!')
    home_directory = settings['homeDirectory']
    temp_directories = settings['tempDirectories']

    for folder in temp_directories:
        target = '{}/{}'.format(home_directory, folder)
        issue_delete(target)


if __name__ == '__main__':
    main()
