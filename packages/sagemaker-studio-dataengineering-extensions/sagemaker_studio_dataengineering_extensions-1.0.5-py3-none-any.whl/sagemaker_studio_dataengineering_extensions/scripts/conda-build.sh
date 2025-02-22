#!/bin/bash

# Initialize conda
eval "$(conda shell.bash hook)"

# Set the name of the Conda environment
ENV_NAME="build-env"

# Check if the environment already exists
if conda info --envs | grep -q $ENV_NAME; then
    echo "Conda environment '$ENV_NAME' already exists."
else
    echo "Creating Conda environment '$ENV_NAME'..."
    conda env create -n $ENV_NAME -f scripts/environment.yaml
    echo "Conda environment '$ENV_NAME' has been created."
fi

# Activate the environment
echo "Activating Conda environment '$ENV_NAME'..."
conda activate $ENV_NAME

echo "Conda environment '$ENV_NAME' is now active."

# clean uncessary folders and cache
rm -rf build/ .hatch __pycache__ .pytest_cache .venv .npmrc

echo "Cleaned cache and lib folder"

# start to build extension

echo "Starting to build extension"

CONDA_BUILD=1 conda build . --python 3.11 --package-format 1 -c conda-forge

CONDA_BUILD=1 conda build . --python 3.12 --package-format 1 -c conda-forge

conda deactivate