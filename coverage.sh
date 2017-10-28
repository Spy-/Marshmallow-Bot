#!/usr/bin/env bash

# Don't let CDPATH interfere with the cd command
unset CDPATH
cd "$(dirname "$0")"


# Execute the bot
exec coverage xml
exec set CODACY_PROJECT_TOKEN=8032b61c2d974b30b46bd1f7f19f95a5
exec python-codacy-coverage -r coverage.xml