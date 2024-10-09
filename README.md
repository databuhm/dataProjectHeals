# dataProjectHeals
This repository documents the analysis of Electronic Medical Records (EMR) data. The primary goal of this project is to **process and load data into BigQuery** for various analytical purposes.

## Overview
**DataProjectHeals** focuses on the analysis of healthcare data using advanced data processing techniques to ensure accurate and reliable data ingestion into Google BigQuery. The project deals with large-scale CSV and SAS (`.sas7bdat`) files, with special attention given to data integrity and encoding validation.

The key objectives of this project are:
1. **Encoding Verification**: Check the encoding of large CSV and SAS files to ensure they are read correctly without data corruption.
2. **Data Loading**: Load the verified and cleaned datasets into Python DataFrames while maintaining the integrity of values and data types.
3. **BigQuery Ingestion**: Upload each processed DataFrame into Google BigQuery as individual tables, enabling scalable SQL-based data analysis.

The following technologies and tools have been used:

- **Programming Languages**: Python, BigQuery
- **Database**: Google BigQuery
- **Data Formats**: `.sas7bdat`, `.csv`

## Features
- Efficient handling of large-scale healthcare datasets to prevent data corruption.
- Verification of file encodings to ensure the integrity of imported data.
- Seamless loading of large datasets into DataFrames for further processing.
- BigQuery ingestion modules for scalable and efficient data analysis.

## Getting Started
### Prerequisites
1. **Python 3.8 or above**: Ensure Python is installed on your system.
2. **BigQuery API Access**: Set up Google Cloud credentials to access the BigQuery datasets.
3. Required Python packages:
   - `pandas`
   - `numpy`
   - `google-cloud-bigquery`
   - `google-cloud-bigquery-storage`
   - `pyarrow`
   - `pyreadstat`
   - `db-dtypes`
   - `chardet`

### Installation

The required dependencies for this project are listed in the `environment.yaml` file. Clone the repository and set up the environment:

```bash
git clone https://github.com/databuhm/dataProjectHeals.git
cd dataProjectHeals
conda env create -f environment.yaml
conda activate dataProjectHeals
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.