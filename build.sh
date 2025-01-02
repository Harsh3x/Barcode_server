#!/bin/bash

# Update the package list
apt-get update

# Install zbar tools and library
apt install libzbar0
apt-get install -y zbar-tools libzbar0

# Install additional system dependencies that pyzbar might require
apt-get install -y gcc python3-dev

# Install Python dependencies
pip install -r requirements.txt
