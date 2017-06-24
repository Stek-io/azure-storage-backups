# Azure Storage Account Backups

Create periodical backups of an Azure Storage Account.

_Under Development_

## Requirements
- python 3

## Setup Environment
- pip install -r requirements.txt

## Run the backups
- copy config.yml into config-production.yml
- edit the config-production.yml file and define the following properties:
  - user: Azure Username
  - pass: Azure Password
  - storage_account_name: the name of the Azure Storage Account
  - storage_account_key: an access key for the Storage Account
  - backup_directory: full path to the backup directory
- run: `app/start.py --config-file <path to config config-production.yml>`

## Output

Azure Storage Backups will create the following directory structure under the backup directory:
```
.
├── [Year]
│   └── [Month]
│       ├── [Day]
│       │   ├── [Archives of the file found under the Storage Account]
│       │   ├── ...
```

For example: 

```
.
├── 2017
│   └── 06
│       ├── 23
│       │   ├── bytecode-discourse-27-2017.06.23.01.tar.gz
│       │   ├── fastmovingtargets-discourse-93-2017.06.23.01.tar.gz
```

## Known Limitations (under development)
- Only daily backups are available
- No scheduling is available
- Old backups are not removed