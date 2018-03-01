# System Administration Scripts
My utility scripts for common server/backup tasks powered by python 3.6!

## **Common Information**
Logs are generated and saved to files based on the directory specified by the
environment variable `BACKUP_DIR` (THIS MUST BE SET IN ORDER TO DO ANYTHING).

## **backup.py**
A script for backing up files to another location local/remote.

The script requires that a user creates a settings.json file which looks like:

```js
{
    "homeDirectory": "<a starting point, I recommend $HOME path>",
    "sourceDirectories": [
                            "directoryA",
                            "directoryB",
                            "ETC"
                        ],
  "backupDestination": "<some location you want to back up to>",
  "tempDirectories": [
                            "<Directories to delete files from>"
                    ]
}

```

Please note rsync is required (comes with most linux distros and mac).

For remote servers rsa key authentication will be required.


## **clean_temp_directories.py**
A script for cleaning out marked directories.

The script requires the same settings.json file from above and uses the 
`tempDirectories` property to know which directories to target for clean up.

