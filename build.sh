#!/bin/bash

# Update the package list and install required dependencies
apt-get update
apt-get install -y zbar-tools libzbar0

# Install Python dependencies
pip install -r requirements.txt
