#!/usr/bin/env bash

# Don't let CDPATH interfere with the cd command
unset CDPATH
cd "$(dirname "$0")"


# Execute the bot
exec coverage run run.py