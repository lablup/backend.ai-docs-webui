#!/bin/bash
set -e
cd "$(dirname "$0")"

# Release version: 19.09.1, 20.03.2a, etc
VERSION=$1
if [[ -z $VERSION ]]; then
    echo "Please enter the release version!"
    exit -1
fi

echo
echo "Current release version:" $(cat docs/VERSION)
echo "Release $VERSION?"
read -p "- type 'yes' to proceed: " yn
if [ "$yn" != "yes" ] ; then
    echo "Release cancelled."
    exit;
fi

# Update version
echo "$VERSION" >| docs/VERSION
echo "docs/VERSION updated."

# Bump to next version
git add -u
git commit -m "Bump version to $VERSION"
git tag -a "$VERSION" -m "Web-UI User Manual v$VERSION"
git push -u origin main
git push -u origin main --tags
echo "Bumped version to $VERSION."
