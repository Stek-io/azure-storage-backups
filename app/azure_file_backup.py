import os
import logging
import shutil
import time
import tarfile

from azure.common import AzureHttpError
from azure.storage.file.fileservice import FileService
from azure.storage.file import models

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Azure Manager"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))


class AzureFileBackup(object):
    """
    Azure Backup Processor
    """

    def __init__(self, config, logger=None):
        """
        Constructor

        :param config: Azure configuration and credentials
        :param logger: A python logger
        """

        # Store state
        self.config = config
        self._backup_directory = config['backup_directory']
        self._file_service = FileService(
            account_name=self.config['file']['storage_account_name'],
            account_key=self.config['file']['storage_account_key'])

        # Create logger if None is provided
        if logger is not None:
            self._logger = logger
        else:
            # log_format = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s' @@@ DIMI => this throws an error
            log_format = '%(asctime)-15s %(message)s'
            logging.basicConfig(format=log_format)
            self._logger = logging.getLogger("azure_manager")
            self._logger.setLevel("DEBUG")

    def download_daily(self):
        """
        Downloads All Azure Files under the give account

        :param account_name: The name of the account
        :param account_key: An access key for the account
        """

        # Construct the daily backup dir
        daily_backup_dir = "%s/%s" % (self._backup_directory, time.strftime("%Y/%m/%d"))

        # Create backup dir for the day
        os.makedirs(daily_backup_dir, exist_ok=True)

        # Get a list of all shares
        shares_generator = self._file_service.list_shares()

        for share in shares_generator:
            self._logger.info("Starting download of share '%s' contents" % share.name)
            target_directory = "%s/%s" % (daily_backup_dir, share.name)
            self.download_share(share_name=share.name, target_directory=target_directory)

            # Share download complete; pause for a bit
            self._logger.info("Pausing for 1 sec...")
            time.sleep(1)

        self._logger.info("Finished backup successfully.")

    def download_share(self, target_directory, share_name):
        """

        :param share_name:
        :return:
        """

        # Ensure directory Exists
        os.makedirs(target_directory, exist_ok=True)

        files = self._file_service.list_directories_and_files(share_name)
        for file in files:
            node_type = type(file)
            if node_type is models.Directory:
                new_target_directory = "%s/%s" % (target_directory, file.name)
                self.download_directory(share_name=share_name, source_directory=file.name,
                                        target_directory=new_target_directory)
            elif node_type is models.File:
                self.download_file(share_name=share_name, source_filename=file.name,
                                   source_directory="",
                                   target_directory=target_directory)
            else:
                self._logger.warning("Unknown file type: %s" % node_type)

        self._logger.info("Archiving Share...")

        # Create date stamp
        tar_filename = '%s-%s.tar.gz' % (target_directory, time.strftime("%Y.%m.%d.%H"))
        with tarfile.open(tar_filename, mode='w:gz') as archive:
            archive.add(name=target_directory, arcname=share_name, recursive=True)

        self._logger.info("Removing original files...")
        shutil.rmtree(target_directory)

    def download_directory(self, share_name, target_directory, source_directory):
        """
        Download a single directory to the given destination

        :param target_directory: The target directory of the copy
        :param source_directory:
        """
        self._logger.info("Downloading directory %s of share %s to %s" % (
            source_directory, share_name, target_directory))

        # Create dir if not exists
        os.makedirs(target_directory, exist_ok=True)

        files = self._file_service.list_directories_and_files(share_name, source_directory)
        for file in files:

            # Check if it's a directory or a file
            node_type = type(file)
            if node_type is models.Directory:
                new_target_directory = "%s/%s" % (target_directory, file.name)
                new_source_dir = "%s/%s" % (source_directory, file.name)
                self.download_directory(share_name=share_name,
                                        target_directory=new_target_directory,
                                        source_directory=new_source_dir)
            elif node_type is models.File:
                self.download_file(share_name=share_name, source_filename=file.name,
                                   source_directory=source_directory,
                                   target_directory=target_directory)
            else:
                self._logger.warning("Unknown file type: %s" % node_type)

    def download_file(self, share_name, source_directory, source_filename, target_directory):
        """

        :param target_directory: The target directory of the copy
        :param file: The file to download
        """
        file_path = "%s/%s" % (target_directory, source_filename)
        self._logger.debug("Downloading file %s to %s" % (source_filename, target_directory))
        try:
            self._file_service.get_file_to_path(share_name=share_name,
                                                directory_name=source_directory,
                                                file_name=source_filename, file_path=file_path)
        except (FileNotFoundError, AzureHttpError):
            self._logger.exception(
                "Failed downloading file %s to %s" % (source_filename, target_directory))

    class AzureBackupException(Exception):
        """
        Custom Exception
        """
