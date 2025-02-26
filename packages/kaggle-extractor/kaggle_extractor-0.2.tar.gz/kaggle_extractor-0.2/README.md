# Kaggle Dataset Downloader

## Overview
This package provides a convenient function to download and extract datasets from Kaggle using the Kaggle API.

## Installation
Ensure that you have the Kaggle API set up on your system. If you haven't configured it yet, follow these steps:

1. Create an account on [Kaggle](https://www.kaggle.com/).
2. Go to "Account" settings and generate a new API token.
3. Place the downloaded `kaggle.json` file in `~/.kaggle/` (Linux/Mac) or `%USERPROFILE%\.kaggle\` (Windows).
4. Install the Kaggle API package if you haven't already:
   ```sh
   pip install kaggle
   ```

## Usage
This package provides a function to download and extract a specific file from a Kaggle dataset.

### Function: `download_and_extract_kaggle_dataset`

#### Parameters:
- `dataset` (str): The Kaggle dataset identifier (e.g., `'zillow/zecon'`).
- `file_name` (str): The specific file within the dataset to download.
- `path` (str, optional): Directory where the file should be saved. Defaults to `'./'`.
- `force` (bool, optional): Whether to force the download if the file already exists. Defaults to `False`.
- `quiet` (bool, optional): Whether to suppress output. Defaults to `True`.
- `licenses` (list, optional): List of accepted licenses. Defaults to `[]`.
- `delete_after_download` (bool, optional): Whether to delete the ZIP file after extraction. Defaults to `True`.

### Example Usage:
```python
download_and_extract_kaggle_dataset('aiaiaidavid/the-big-dataset-of-ultra-marathon-running','TWO_CENTURIES_OF_UM_RACES.csv')
```


## License
This project is released under the MIT License.

