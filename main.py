import argparse
from pathlib import Path
from folder_sync_service import FolderSyncService


def main():
    """Main function to parse command-line arguments and start synchronization."""
    parser = argparse.ArgumentParser(description='Synchronize source folder with the replica folder')
    parser.add_argument("source_path", type=Path, help="Path to the source folder")
    parser.add_argument("replica_path", type=Path, help="Path to the replica folder")
    parser.add_argument("sync_interval", type=int, help="Interval between synchronization runs (in seconds)")
    parser.add_argument("log_file_path", type=Path, help="Path to the log file")
    args = parser.parse_args()

    # Create an instance of FolderSyncService
    folder_sync_service = FolderSyncService(args.source_path, args.replica_path, args.sync_interval, args.log_file_path)

    # Start synchronization loop
    folder_sync_service.run_sync_loop()


if __name__ == "__main__":
    main()
