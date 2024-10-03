#!/bin/bash

# Check if the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    # Try to activate the virtual environment automatically
    if [ -f "venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    else
        echo "Error: Virtual environment not found!"
        echo "Please activate the virtual environment manually or ensure it's located in 'venv/'."
        exit 1
    fi
else
    echo "Virtual environment is already activated."
fi
