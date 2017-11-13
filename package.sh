#!/bin/bash

set -e

BUILD_DIR=./build
SRC_DIR=./src
ASSETS_DIR=./assets

ZIP_FILE=lambda.zip

# Copy source
mkdir -p $BUILD_DIR
cp -a $SRC_DIR/* $BUILD_DIR/
pip install -r $SRC_DIR/requirements.txt -t $BUILD_DIR > /dev/null
cp -a $ASSETS_DIR $BUILD_DIR

# Create the zip
cd $BUILD_DIR
zip -9 -r ../$ZIP_FILE ./ >/dev/null
cd ..

# Clean up
rm -r $BUILD_DIR
