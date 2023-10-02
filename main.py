import os
import json
import pandas as pd
from absl import app, flags
from concurrent.futures import ThreadPoolExecutor

# Define flags
FLAGS = flags.FLAGS
flags.DEFINE_string("input_directory", "./dataset", "Path to the input directory")
flags.DEFINE_string("output_directory", "./output", "Path to the output directory")

def extract_english_data(english_file):
    english_data = {}
    
    with open(english_file, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            id = data["id"]
            english_data[id] = {
                "en_utt": data["utt"],
                "en_annot_utt": data["annot_utt"]
            }
    
    return english_data

def create_translation_file(english_data, input_file, output_directory):
    language_code = os.path.basename(input_file).split("-")[0]
    output_filename = os.path.join(output_directory, f"en-{language_code}.xlsx")
    translation_data = pd.DataFrame(columns=["id", "en_utt", "en_annot_utt", f"{language_code}_utt", f"{language_code}_annot_utt"])

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            id = data["id"]
            
            if id in english_data:
                english_row = english_data[id]
                translation_data.loc[len(translation_data)] = {
                    "id": id,
                    "en_utt": english_row["en_utt"],
                    "en_annot_utt": english_row["en_annot_utt"],
                    f"{language_code}_utt": data["utt"],
                    f"{language_code}_annot_utt": data["annot_utt"]
                }

    translation_data.to_excel(output_filename, index=False)

def main(argv):
    input_directory = FLAGS.input_directory
    output_directory = FLAGS.output_directory

    # Find and process 'en-US.jsonl' file to extract English data
    english_file = os.path.join(input_directory, "en-US.jsonl")
    english_data = extract_english_data(english_file)

    # Process translation files for other languages
    with ThreadPoolExecutor() as executor:
        for filename in os.listdir(input_directory):
            if filename.endswith(".jsonl") and filename != "en-US.jsonl":
                input_file = os.path.join(input_directory, filename)
                executor.submit(create_translation_file, english_data, input_file, output_directory)

if __name__ == "__main__":
    app.run(main)