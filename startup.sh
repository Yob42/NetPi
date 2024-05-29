#!/bin/bash

# Define the project root directory
PROJECT_ROOT="/home/admin/projects/speedtest"

# Define the virtual environment name
VENV_NAME="st_env"

# Define the Python requirements file
REQUIREMENTS_FILE="requirements.txt"

# Define the directories to create
DIRECTORIES=("instance" "results" "results/ping" "results/speedtest" "templates")

# Create directories if they don't exist
for dir in "${DIRECTORIES[@]}"; do
    if [ ! -d "$PROJECT_ROOT/$dir" ]; then
        mkdir -p "$PROJECT_ROOT/$dir"
        echo "Created directory: $PROJECT_ROOT/$dir"
    else
        echo "Directory already exists: $PROJECT_ROOT/$dir"
    fi
done

# Install Python and virtual environment tools
sudo apt update
sudo apt install -y python3-pip python3-venv

# Navigate to the project root directory
cd "$PROJECT_ROOT"

# Create or locate the virtual environment
if [ ! -d "$PROJECT_ROOT/$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME"
    echo "Created virtual environment: $PROJECT_ROOT/$VENV_NAME"
else
    echo "Virtual environment already exists: $PROJECT_ROOT/$VENV_NAME"
fi

# Activate the virtual environment
source "$PROJECT_ROOT/$VENV_NAME/bin/activate"

# Install the Python dependencies from requirements.txt
if [ -f "$PROJECT_ROOT/$REQUIREMENTS_FILE" ]; then
    pip install -r "$PROJECT_ROOT/$REQUIREMENTS_FILE"
    echo "Installed dependencies from $REQUIREMENTS_FILE"
else
    echo "Requirements file not found: $PROJECT_ROOT/$REQUIREMENTS_FILE"
fi

# Make all .sh files in the project directory executable
find "$PROJECT_ROOT" -type f -name "*.sh" -exec chmod +x {} \;
echo "Made all .sh files executable in $PROJECT_ROOT"

# Set permissions to 777 recursively
sudo chmod -R 777 "$PROJECT_ROOT"
echo "Set permissions to 777 for $PROJECT_ROOT"

# Change ownership to admin recursively
sudo chown -R admin:admin "$PROJECT_ROOT"
echo "Changed ownership to admin:admin for $PROJECT_ROOT"

echo "Startup script completed."
