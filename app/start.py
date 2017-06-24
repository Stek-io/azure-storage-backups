#!/usr/bin/env python3

import click
import common
import os
from azure_file_backup import AzureFileBackup

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Azure File Storage Backups"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))
__default_config_file__ = "%s/../config/config.yml" % __abs_dirpath__


@click.command()
@click.option('--config-file', required=False, default=__default_config_file__,
              help='Path to config file')
def start(config_file):
    """
    Start Backup Service
    """
    # Load config
    config = common.load_config_file(config_file)

    # Load logging config
    common.setup_logging_config("%s/../config/" % __abs_dirpath__)

    # Get logger
    logger = common.get_logger("app")

    logger.info("Starting backup service...")

    # Download daily
    azure_file_backup = AzureFileBackup(config=config, logger=logger)
    azure_file_backup.download_daily()


if __name__ == '__main__':
    app = start(obj={})
