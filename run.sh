#!/bin/bash
# Bash script to run the Flask application on Unix-like systems

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to handle errors
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

echo -e "${GREEN}=== Weather Dashboard ===${NC}"
echo -e "${YELLOW}Initializing application...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    error_exit "Python 3 is not installed. Please install it first."
fi

# Check if .env file exists, create from .env.example if not
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env || error_exit "Failed to create .env file"
    echo -e "${GREEN}.env file created successfully${NC}"
fi

# Load environment variables from .env file
set -a
source .env
set +a

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv || error_exit "Failed to create virtual environment"
    echo -e "${GREEN}Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate || error_exit "Failed to activate virtual environment"

# Install/upgrade dependencies
echo -e "${GREEN}Installing/upgrading dependencies...${NC}"
python -m pip install --upgrade pip || error_exit "Failed to upgrade pip"
pip install -r requirements.txt || error_exit "Failed to install dependencies"

# Set Flask environment variables
export FLASK_APP=run.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Clear the screen and show application info
clear
echo -e "${GREEN}=== Weather Dashboard ===${NC}"
echo -e "${YELLOW}Server is starting up...${NC}"
echo -e "${YELLOW}Server will be available at: http://127.0.0.1:5000/${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo

# Run the Flask application
flask run --host=0.0.0.0 --port=5000
