import os


def get_csv_files_from_download(download_path=None):
    if download_path is None:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(download_path):
        raise ValueError(f"The specified download path does not exist: {download_path}")

    # Use glob to find all CSV files in the download directory
    csv_files = [os.path.join(download_path, f) for f in os.listdir(download_path) if f.lower().endswith('.csv')]

    return set(csv_files)

def skip_search(cached_file:str, forced:bool = False) -> bool:
    """
    Check if the file exists and if it should be skipped based on the forced flag.

    :param cached_file: The path to the cached file.
    :param forced: If True, the file will not be skipped even if it exists.
    :return: True if the file should be skipped, False otherwise.
    """
    if not os.path.exists(cached_file):
        return False
    if forced:
        os.remove(cached_file)
        return False
    return True

def get_generated_file(set_of_files, download_path=None) -> str:
    current_files = get_csv_files_from_download(download_path)
    if len(current_files) == 0:
        raise ValueError("No CSV files found in the specified download path.")
    generated_files = current_files - set_of_files
    if len(generated_files) == 0 | len(generated_files) > 1:
        raise ValueError("There should be exactly one new CSV file generated.")
    return generated_files.pop()


def move_generated_file(original_path, destination_path):
    if not os.path.exists(original_path):
        raise FileNotFoundError(f"The original file does not exist: {original_path}")

    dir_path = os.path.dirname(destination_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    os.rename(original_path, destination_path)
    return destination_path
