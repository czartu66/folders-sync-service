import shutil
from pathlib import Path
from hashlib import md5
import time
import logging


class FolderSyncService:
    def __init__(self, source_path: Path, replica_path: Path, sync_interval: int, log_file_path: Path):
        self.source_path = source_path
        self.replica_path = replica_path
        self.sync_interval = sync_interval
        self.log_file_path = log_file_path
        self.source_file_info = {}  # Stores information about source files
        self.replica_file_info = {}  # Stores information about replica files

        # Configure logging
        self._configure_logging()

        # Check if source folder exists
        if not self.source_path.exists():
            raise ValueError(f"Provided source folder path does not exist")

        # Check if replica folder exists
        if not self.replica_path.is_dir():
            self.replica_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Replica folder: '{self.replica_path}' created")

    def _configure_logging(self):
        """Configure logging to both file and console."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create file handler and set level to INFO
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)

        # Create console handler and set level to INFO
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    @staticmethod
    def _get_file_info(folder_path: Path) -> dict[Path, str]:
        """
        Getting information about files in a directory: file paths and md5.
        :param folder_path:
        :return: Dictionary with file path as key and file checksum as value
        """
        file_info = {}
        for file in folder_path.glob('**/*'):
            if file.is_file():
                checksum = md5(file.read_bytes()).hexdigest()
                file_info[file.relative_to(folder_path)] = checksum
        return file_info

    def _sync_dirs(self):
        """
        This method synchronizes two folders: source and replica.
        """
        self.source_file_info = self._get_file_info(self.source_path)
        self.replica_file_info = self._get_file_info(self.replica_path)

        # Check if in replica folder there is a file which is not in source and remove if needed
        for relative_path, checksum in self.replica_file_info.items():
            if relative_path not in self.source_file_info:
                file = self.replica_path / relative_path
                file.unlink()
                self.logger.info(f"File {file} removed from replica")

        # Check if in source folder there is a file which is not in replica and copy if needed
        for relative_path, checksum in self.source_file_info.items():
            source_file = self.source_path / relative_path
            replica_file = self.replica_path / relative_path
            replica_checksum = self.replica_file_info.get(relative_path)

            # Create parent directories in replica path if they don't exist
            replica_file.parent.mkdir(parents=True, exist_ok=True)

            if not replica_file.exists() or replica_checksum != checksum:
                # If the source file is a directory, use shutil.copytree to copy recursively
                if source_file.is_dir():
                    shutil.copytree(source_file, replica_file, dirs_exist_ok=True)
                    self.logger.info(f"Folder {source_file} copied to {replica_file}")
                else:
                    shutil.copy2(source_file, replica_file)
                    self.logger.info(f"File {source_file} copied to {replica_file}")

    def run_sync_loop(self):
        """Run synchronization in a loop with the specified interval."""
        iteration_number = 1
        while True:
            self._sync_dirs()
            iteration_number += 1
            time.sleep(self.sync_interval)
