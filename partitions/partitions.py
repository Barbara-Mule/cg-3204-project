import json

def separate_partition_data(input_file, output_directory):
    partition_data = {"test": [], "train": [], "dev": []}

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            partition = data.get("partition", "unknown")

            # Check if the partition is one of the specified values
            if partition in partition_data:
                partition_data[partition].append(data)

    for partition, data_list in partition_data.items():
        output_file = f"{output_directory}/{partition}-{language}.jsonl"
        with open(output_file, "w", encoding="utf-8") as outfile:
            for data in data_list:
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write("\n")

if __name__ == "__main__":
    languages = ["en-US", "sw-KE", "de-DE"]
    output_directory = "partitions/output"

    for language in languages:
        input_file = f"dataset/{language}.jsonl"
        separate_partition_data(input_file, output_directory)

    print("Separation completed.")
