#!/bin/bash

# Install system dependencies for zbar
apt-get update
apt-get install -y zbar-tools libzbar0

# Install Python dependencies
pip install -r requirements.txt
