#!/bin/bash

# Prompt the user for the path to the 'main.py' script (defaults to "main.py")
read -p "Enter the path to the 'main.py' script (defaults to 'main.py'): " MAIN_SCRIPT
MAIN_SCRIPT=${MAIN_SCRIPT:-"main.py"}

# Prompt the user for the path to the parent directory containing batched folders (defaults to "batched_dataset")
read -p "Enter the path to the parent directory containing batched folders (defaults to 'batched_dataset'): " PARENT_DIRECTORY
PARENT_DIRECTORY=${PARENT_DIRECTORY:-"batched_dataset"}

# Prompt the user for the path to the output directory (defaults to "output")
# Prompt the user for the path to the output directory (defaults to "output")

read -p "Enter the path to the output directory (defaults to 'output'): " OUTPUT_DIRECTORY
OUTPUT_DIRECTORY=${OUTPUT_DIRECTORY:-"output"}

# Check if the provided 'main.py' script exists
if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "'main.py' script '$MAIN_SCRIPT' not found."
    exit 1
fi
#check if the provided parent directory exists
# Check if the provided parent directory exists
if [ ! -d "$PARENT_DIRECTORY" ]; then
    echo "Parent directory '$PARENT_DIRECTORY' does not exist."
    exit 1
fi

# Check if the provided output directory exists; if not, create it
if [ ! -d "$OUTPUT_DIRECTORY" ]; then
    mkdir -p "$OUTPUT_DIRECTORY"
fi

# Loop through batched folders and call 'main.py' for each
for batch_directory in "$PARENT_DIRECTORY"/*; do
    if [ -d "$batch_directory" ]; then
        echo "Processing batch: $(basename "$batch_directory")"
        python "$MAIN_SCRIPT" --input_directory "$batch_directory" --output_directory "$OUTPUT_DIRECTORY"
    fi
done

echo "Processing completed for all batched folders."