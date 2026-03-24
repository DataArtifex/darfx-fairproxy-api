#!/bin/bash

# Simple script to rename the project and package
# Usage: ./rename.sh "new-project-name" "new_package_name"

OLD_PROJECT="dartfx-workspace"
OLD_PACKAGE="workspace"

NEW_PROJECT=$1
NEW_PACKAGE=$2

if [ -z "$NEW_PROJECT" ] || [ -z "$NEW_PACKAGE" ]; then
    echo "Usage: ./rename.sh <new-project-name> <new_package_name>"
    echo "Example: ./rename.sh my-cool-app my_cool_app"
    exit 1
fi

echo "Renaming project from $OLD_PROJECT to $NEW_PROJECT"
echo "Renaming package from $OLD_PACKAGE to $NEW_PACKAGE"

# 1. Rename the package directory
# First, rename the hatch_foo directory to the new package name
if [ -d "src/dartfx/hatch_foo" ]; then
    mv "src/dartfx/hatch_foo" "src/dartfx/$NEW_PACKAGE"
fi

# Also handle if it was already renamed to OLD_PACKAGE
if [ -d "src/dartfx/$OLD_PACKAGE" ]; then
    mv "src/dartfx/$OLD_PACKAGE" "src/dartfx/$NEW_PACKAGE"
fi

# 2. Remove stale lock files and environments if they exist
rm -f uv.lock
rm -rf .hatch/
rm -rf .venv/

# 3. Replace strings in files
# Using LC_ALL=C to avoid sed issues on macOS with non-UTF8 characters if any
# We use -i '' for macOS compatibility (sed)
# We also exclude __pycache__ and hidden files to avoid processing binary or system files

export LC_ALL=C
export LANG=C

# Replace template placeholders and project/package names
find . -type f \
  -not -path '*/.*' \
  -not -path '*/__pycache__/*' \
  ! -name "*.pyc" \
  ! -name ".DS_Store" \
  ! -name "rename.sh" \
  -exec sed -i '' "s/hatch-foo/$NEW_PROJECT/g" {} +

find . -type f \
  -not -path '*/.*' \
  -not -path '*/__pycache__/*' \
  ! -name "*.pyc" \
  ! -name ".DS_Store" \
  ! -name "rename.sh" \
  -exec sed -i '' "s/hatch_foo/$NEW_PACKAGE/g" {} +

find . -type f \
  -not -path '*/.*' \
  -not -path '*/__pycache__/*' \
  ! -name "*.pyc" \
  ! -name ".DS_Store" \
  ! -name "rename.sh" \
  -exec sed -i '' "s/$OLD_PROJECT/$NEW_PROJECT/g" {} +

find . -type f \
  -not -path '*/.*' \
  -not -path '*/__pycache__/*' \
  ! -name "*.pyc" \
  ! -name ".DS_Store" \
  ! -name "rename.sh" \
  -exec sed -i '' "s/$OLD_PACKAGE/$NEW_PACKAGE/g" {} +

find . -type f \
  -not -path '*/.*' \
  -not -path '*/__pycache__/*' \
  ! -name "*.pyc" \
  ! -name ".DS_Store" \
  ! -name "rename.sh" \
  -exec sed -i '' "s/DataArtifex\/$OLD_PROJECT/DataArtifex\/$NEW_PROJECT/g" {} +

echo "Done! Please verify changes and run 'uv sync'."
