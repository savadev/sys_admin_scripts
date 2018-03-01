# System Administration Scripts
My utility scripts for common server/backup tasks powered by python 3.6!

## **Backup.py**
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
  "backupDestination": "<some location you want to back up to>"
}

```

Please note rsync is required (comes with most linux distros and mac).

For remote servers rsa key authentication will be required.
