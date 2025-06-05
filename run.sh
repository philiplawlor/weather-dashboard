#!/bin/bash
# Bash script to run the Flask application on Unix-like systems

echo "Setting up Python virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment"
    exit 1
fi

source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    exit 1
fi

echo "Starting the application..."
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
