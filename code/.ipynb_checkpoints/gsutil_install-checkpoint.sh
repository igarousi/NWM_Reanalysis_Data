#!/bin/bash
# Run this script to install gsutil

# Download the tar file (gsutil.tar.gz)
wget https://storage.googleapis.com/pub/gsutil.tar.gz -P $HOME/software

# Unzip it to your Home directory
tar -xf $HOME/software/gsutil.tar.gz -C $HOME/software

# Add gsutil to PATH environment variable
export PATH=${PATH}/:$HOME/software/gsutil

# Update
cd $HOME/software/gsutil
./gsutil update