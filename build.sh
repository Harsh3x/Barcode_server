#!/bin/bash

# Update the package list
apt-get update
apt-get update

# Install zbar tools and library
apt-get install -y zbar-tools libzbar0

# Install additional system dependencies that pyzbar might require
apt-get install -y gcc python3-dev

# Install Python dependencies from requirements.txt
pip install -r requirements.txt
