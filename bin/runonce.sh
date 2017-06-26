#!/usr/bin/env bash

# Get full path to the directory of this file
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null

VENV_NAME="venv"

LOGO="
==========================================
=====   AZURE FILE STORAGE BACKUPS   =====
==========================================
"

# Print some intro
echo "$LOGO"

echo "Starting AZURE FILE STORAGE BACKUPS..."

# Go into the app root directory
cd "$SCRIPTPATH/../"

# Activate Virtual Env
source "$VENV_NAME/bin/activate"

CONFIG_FILE=${1:-./config/config.yml}

# Run script
python3 ./app/start.py --config-file $CONFIG_FILE

deactivate