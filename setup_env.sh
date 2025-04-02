#!/bin/bash

set -e  # Exit immediately if any command fails

echo "Starting environment setup..."
echo "------------------------------"

# Create the virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "env"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "env/bin/activate"

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r "requirements.txt"
    echo "Dependencies installed from requirements.txt"
else
    echo "Error: requirements.txt not found in $(pwd)" >&2
    exit 1
fi

# Set default environment variables
echo "Configuring environment variables..."
export PYTHONPATH="$PWD"
export PROJECT_ROOT="$PWD"

echo "------------------------------"
echo "Environment setup completed successfully!"
echo "You are now in the virtual environment. To exit, run 'deactivate'."