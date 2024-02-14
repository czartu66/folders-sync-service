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

        # Check if source folder exists
        if not self.source_path.exists():
            raise ValueError(f"Provided source folder path does not exist")

        # Check if replica folder exists
        if not self.replica_path.is_dir():
            self.replica_path.mkdir(parents=True, exist_ok=True)
            print(f"Replica folder created under the following path: {self.replica_path}")

        # Configure logging
        self._configure_logging()

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
    def _get_file_info(folder_path: Path) -> dict[str, Path]:
        """
        Getting information about files in a directory: file paths and md5.
        :param folder_path:
        :return: Dictionary with file path as key and file checksum as value
        """
        file_info = {}
        for file in folder_path.glob('**/*'):
            if file.is_file():
                checksum = md5(file.read_bytes()).hexdigest()
                file_info[checksum] = file

        return file_info

    def _get_replica_checksum(self, file_path: Path):
        """
        Get the checksum from replica file info based on source file path.
        """
        relative_path = file_path.relative_to(self.source_path)
        for checksum, path in self.replica_file_info.items():
            if path.relative_to(self.replica_path) == relative_path:
                return checksum
        return None

    def _sync_dirs(self):
        """
        This method synchronizes two folders: source and replica.
        """
        self.source_file_info = self._get_file_info(self.source_path)
        self.replica_file_info = self._get_file_info(self.replica_path)

        # Check if in replica folder there is a file which is not in source and remove if needed
        for checksum in self.replica_file_info:
            if checksum not in self.source_file_info:
                file = self.replica_file_info[checksum]
                file.unlink()
                self.logger.info(f"File {file} removed")

        # Check if in source folder there is a file which is not in replica and copy if needed
        # When the checksums don't match - replace it
        for src_checksum, file_path in self.source_file_info.items():
            replica = self.replica_path / file_path.relative_to(self.source_path)
            replica_checksum = self._get_replica_checksum(file_path)
            if not replica.exists() or replica_checksum != src_checksum:
                shutil.copy2(file_path, replica)
                self.logger.info(f"File {file_path} copied to File {replica}")

    def run_sync_loop(self):
        """Run synchronization in a loop with the specified interval."""
        iteration_number = 1
        while True:
            # self.logger.info(f"This is {iteration_number} iteration")
            self._sync_dirs()
            iteration_number += 1
            time.sleep(self.sync_interval)
