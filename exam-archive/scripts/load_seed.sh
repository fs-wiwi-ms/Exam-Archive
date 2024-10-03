#!/bin/bash

# Source the shared virtual environment check script
source ./scripts/check_venv.sh

# Directory where seed files are stored
SEED_DIR="seed"

# Ensure the seed directory exists and has seed files
if [ ! -d "$SEED_DIR" ] || [ -z "$(ls -A $SEED_DIR/*.json 2>/dev/null)" ]; then
    echo "No seed files found in $SEED_DIR"
    exit 1
fi

# List all available seed files
echo "Available seed files:"
seed_files=($(ls -1 $SEED_DIR/*.json))
for i in "${!seed_files[@]}"; do
    echo "$((i + 1)). ${seed_files[$i]##*/}"
done

# Prompt the user to select a seed file
read -p "Select a seed file to load (enter number): " choice

# Validate input
if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -le 0 ] || [ "$choice" -gt "${#seed_files[@]}" ]; then
    echo "Invalid selection!"
    exit 1
fi

# Get the selected seed file
selected_seed_file=${seed_files[$((choice - 1))]}

# Load the selected seed file using Django's loaddata
echo "Loading seed file: $selected_seed_file"
python manage.py loaddata "$selected_seed_file"

# Check if the load was successful
if [ $? -eq 0 ]; then
    echo "Seed file loaded successfully!"
else
    echo "Failed to load seed file!"
fi
