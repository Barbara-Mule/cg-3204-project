# ICS 3204: Computer Graphics CAT 1

### Prerequisites
Install all the required dependencies

```bash
conda install --file requirements.txt
```

#### Question 1
The approach taken was to split the dataset into batches that can then be processed in parallel using multithreading. To split the dataset, execute the `splitter.sh` script.

To generate the translation `.xlxs` files run the `generator.sh` script.

#### Question 2
Run the `partitions.py` script to generate the partitions.
```bash
python partitions/partitions.py
```

#### Question 4
Run the `trainsets.py` script to generate the json file with the translations for the train set partitions.
```bash
python partitions/trainsets.py
```
