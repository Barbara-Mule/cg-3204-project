import json
import glob

def extract_english_data(english_file):
    english_data = {}
    
    with open(english_file, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            id = data["id"]
            en_utt = data["utt"]
            english_data[id] = en_utt
    
    return english_data

def merge_train_data(input_directory, output_file, english_file):
    english_data = extract_english_data(english_file)
    translation_data = []

    # Find all JSONL files in the input directory starting with "train-"
    jsonl_files = glob.glob(f"{input_directory}/train-*.jsonl")

    for jsonl_file in jsonl_files:
        language_code = jsonl_file.split("/")[-1].split("-")[1]

        with open(jsonl_file, "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line.strip())
                id = data["id"]
                xx_utt = data["utt"]
                en_utt = english_data.get(id, "")

                translation_data.append({
                    "id": id,
                    "en_utt": en_utt,
                    f"{language_code}_utt": xx_utt
                })

    # Write the merged data to a single JSON file
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(translation_data, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_directory = "partitions/output" 
    output_file = "partitions/merged_train_data.json" 
    english_file = "partitions/output/train-en-US.jsonl"

    merge_train_data(input_directory, output_file, english_file)

    print(f"Merged train data saved to {output_file}.")
