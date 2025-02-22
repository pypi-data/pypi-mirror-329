#!/usr/bin/env bash

#
# This script synchronizes the required Python version, dependencies, and
# dependency versions from the project config to the script inline metadata.
#

set -euo pipefail

# Path to the script.
script="$1"

# Get everything before the script block.
head=$(sed '/^# \/\/\/ script$/q' "$script")

# Get the requires-python and dependencies block.
# Remove null bytes.
# Comment out every line.
# Remove trailing whitespace.
block=$(
  grep \
    --perl-regexp \
    --null-data \
    --only-matching \
    --regexp='(?s)requires-python.+?\]' \
    pyproject.toml \
    | tr -d '\0' \
    | sed 's/^/# /' \
    | sed 's/[[:space:]]\+$//'
)

# Get everything after the script block.
tail=$(awk '/^# \/\/\/$/,EOF' "$script")

# Write the script with the updated inline metadata.
{
  echo "$head"
  echo "#"
  echo "$block"
  echo "#"
  echo "$tail"
} > "$script"
