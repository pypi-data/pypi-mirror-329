# PredDNAContam

PredDNAContam is a tool for DNA contamination prediction from biosample data.

## Input File Format (CSV)

When using **PredDNAContam**, your input data should be in CSV format with the following columns:

| Column  | Description |
|---------|------------|
| GQ      | Genotype quality |
| DP      | Total read depth |
| AF      | Allele frequency |
| VAF     | Variant allele frequency |

### Example CSV File

```csv
GQ,DP,AF,VAF
20,47,0.5,0.23
60,25,0.5,0.24
23,55,0.5,0.78
...


### Example config.txt file:

Before running PredDNAContam, you need to configure the paths in the config.txt file. This file contains important directory paths and filenames for the model, scaler, and input/output files.

input_dir=/path/to/csv_files
output_dir=/path/to/output_directory/output_PredDNAcontam
model_filename=/path/to/PredDNAContam_model/Random_Forest_Contamination_Model.joblib
scaler_filename=/path/to/PredDNAContam_model_scaler/scaler.joblib


## Installation

You can install this package using:

```bash
pip install PredDNAContam
