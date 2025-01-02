#!/bin/bash

# Update package lists
apt-get update

# Install zbar dependencies
apt-get install -y zbar-tools libzbar0

# Install Python dependencies (use pip if you're not using poetry)
pip install -r requirements.txt
