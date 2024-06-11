#!/bin/bash

# Create python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Download and setup models
cd models || exit

# MXFold2
wget https://github.com/mxfold/mxfold2/releases/download/v0.1.2/mxfold2-0.1.2-cp310-cp310-manylinux_2_17_x86_64.whl
pip3 install mxfold2-0.1.2-cp310-cp310-manylinux_2_17_x86_64.whl

# KnotFold
git clone https://github.com/jbindaAI/KnotFold.git

# RNAstructure
wget https://rna.urmc.rochester.edu/Releases/current/RNAstructureLinuxTextInterfaces64bit.tgz
tar -xzvf RNAstructureLinuxTextInterfaces64bit.tgz
export DATAPATH=$(pwd)/RNAstructure/data_tables

cd ..
