# folders-sync

This Python script synchronizes two folders by maintaining a full, identical copy of the source folder in the replica folder. The synchronization is one-way, ensuring that the content of the replica folder exactly matches the content of the source folder.

## Features

- One-way synchronization from source to replica folder.
- Periodic synchronization based on a specified interval.
- Logging of file creation, copying, and removal operations to a specified log file.
- Command-line arguments for specifying folder paths, synchronization interval, and log file path.
- Uses MD5 hashing to detect changes in file content.
- Implemented using built-in Python libraries without third-party dependencies.

## Usage

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Install Python**: Ensure that Python 3.x is installed on your system.

3. **Navigate to the Repository**: Open a terminal or command prompt and navigate to the directory where the script is located.

4. **Run the Script**: Execute the script with the following command:

    ```bash
    python main.py source_folder replica_folder sync_interval log_file
    ```

    Replace `source_folder`, `replica_folder`, `sync_interval`, and `log_file` with the appropriate values:

    - `source_folder`: Path to the source folder whose content will be synchronized.
    - `replica_folder`: Path to the replica folder where the synchronized content will be stored.
    - `sync_interval`: Synchronization interval in seconds. The script will synchronize the folders periodically based on this interval.
    - `log_file`: Path to the log file where file operations will be logged.

5. **View Logs**: Check the specified log file for details of file operations performed during synchronization.

## Example

```bash
python main.py /path/to/source /path/to/replica 60 /path/to/sync.log
```

This command will synchronize the content of /path/to/source with /path/to/replica every 60 seconds and log the file operations to /path/to/sync.log.


## Notes

- Ensure that the script has the necessary permissions to read from the source folder, write to the replica folder, and create/write to the log file.
- The script will create the replica folder if it does not exist.
- If the replica folder already contains files that are not present in the source folder, they will be removed during synchronization to ensure consistency.
