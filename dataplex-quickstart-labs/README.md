# Dataplex Quickstart for Practitioners

This repository has Dataplex labs for that has minimal automation for the full developer experience. It is meant to provide a sequential introduction to Dataplex using the command line interface.

## Getting set up for the lab

### 1. Clone the git repo

Run in Cloud Shell-
```
cd ~
git clone https://github.com/anagha-google/dataplex-labs-ak.git
```

### 2. Set up working directory

Run in Cloud Shell-
```
cp -r dataplex-labs-ak/dataplex-quickstart-labs ~/
```

### 3. Datasets setup

Run the shell script below that untars a few datasets.
```
# Permissions
chmod +x ~/dataplex-quickstart-labs/00-resources/scripts/bash/dataset_untar.sh

# Untar & remove archives
./dataplex-quickstart-labs/00-resources/scripts/bash/dataset_untar.sh

```





