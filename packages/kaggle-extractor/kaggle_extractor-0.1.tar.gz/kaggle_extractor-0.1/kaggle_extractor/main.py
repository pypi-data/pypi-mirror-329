import kaggle
import zipfile
import os

def download_and_extract_kaggle_dataset(dataset: str, file_name: str, path: str = './', force: bool = False, quiet: bool = True, licenses= [], delete_after_download: bool = True):
   
    # Check if the CSV file already exists in the specified directory
    csv_exists = os.path.exists(os.path.join(path, file_name))
    
    if csv_exists and not force:
        print(f"The file {file_name} already exists. Skipping download.")
        return
    
    # Download the specific file as a ZIP
    kaggle.api.dataset_download_file(
        dataset,
        file_name,
        path,
        force,
        quiet,
        licenses
    )

    zip_file_name = path + file_name + '.zip'

    # Extract the contents of the ZIP file
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(path)
    
    if delete_after_download:  
        os.remove(zip_file_name)
