#!/bin/bash

# Source the shared virtual environment check script
source ./scripts/check_venv.sh

# Directory where seed files are stored
SEED_DIR="seed"
DEFAULT_NAME="BASE"

# Ensure the seed directory exists
mkdir -p $SEED_DIR

# Find the highest seed number in the seed directory
last_number=$(find $SEED_DIR -name '*.json' | sed -E 's/.*\/([0-9]+)_.*\.json/\1/' | sort -nr | head -n1)

# If no files are found, start at 0001
if [ -z "$last_number" ]; then
    next_number=1
else
    next_number=$((last_number + 1))
fi

# Prompt the user for a seed name
read -p "Enter seed name (default: $DEFAULT_NAME): " seed_name

# Use the default name if the user enters nothing
seed_name=${seed_name:-$DEFAULT_NAME}

# Format the new seed file name, adding leading zeros to the number
seed_file=$(printf "%s/%04d_%s.json" "$SEED_DIR" "$next_number" "$seed_name")

# Create the seed file by dumping data using Django's dumpdata command
echo "Creating seed file: $seed_file"
python manage.py dumpdata --exclude auth --exclude contenttypes --exclude sessions --indent 4 > "$seed_file"

# Confirm creation
if [ $? -eq 0 ]; then
    echo "Seed file created successfully: $seed_file"
else
    echo "Failed to create seed file!"
fi
