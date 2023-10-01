#!/bin/bash

# Prompt the user for the input directory path (defaults to "dataset")
read -p "Enter the input directory path (defaults to 'dataset'): " INPUT_DIRECTORY
INPUT_DIRECTORY=${INPUT_DIRECTORY:-"dataset"}

# Prompt the user for the output parent directory path (defaults to "batched_dataset")
read -p "Enter the output parent directory path (defaults to 'batched_dataset'): " OUTPUT_PARENT_DIRECTORY
OUTPUT_PARENT_DIRECTORY=${OUTPUT_PARENT_DIRECTORY:-"batched_dataset"}

# Prompt the user for the batch size (defaults to 10)
read -p "Enter the batch size (defaults to 10): " BATCH_SIZE
BATCH_SIZE=${BATCH_SIZE:-10}

# Check if the provided input directory exists
if [ ! -d "$INPUT_DIRECTORY" ]; then
    echo "Input directory '$INPUT_DIRECTORY' does not exist."
    exit 1
fi

# Create the output parent directory if it doesn't exist
if [ ! -d "$OUTPUT_PARENT_DIRECTORY" ]; then
    mkdir -p "$OUTPUT_PARENT_DIRECTORY"
fi

# List of JSONL files in the input directory (excluding English file)
jsonl_files=$(ls "$INPUT_DIRECTORY"/*.jsonl | grep -v "en-US.jsonl")

# Initialize batch count and batch directory
batch_count=1
batch_directory="$OUTPUT_PARENT_DIRECTORY/batch-$batch_count"

# Create the first batch directory
mkdir -p "$batch_directory"

# Counter to keep track of files in the current batch
file_count=0

# Loop through JSONL files and move them into batch folders
for jsonl_file in $jsonl_files; do
    language_code=$(basename "$jsonl_file" .jsonl | cut -d'-' -f1)

    # Check if the batch is full or a new batch needs to be created
    if [ "$file_count" -eq "$BATCH_SIZE" ]; then
        ((batch_count++))
        batch_directory="$OUTPUT_PARENT_DIRECTORY/batch-$batch_count"
        mkdir -p "$batch_directory"
        file_count=0
    fi

    # Copy 'en-US.jsonl' to the batch directory
    cp "$INPUT_DIRECTORY/en-US.jsonl" "$batch_directory/"

    # Copy the current language's JSONL file to the batch directory
    cp "$jsonl_file" "$batch_directory/"

    ((file_count++))
done

echo "Language files have been split into batches of $BATCH_SIZE."
