def get_csv_files_from_download(download_path=None):
    import os

    if download_path is None:
            download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(download_path):
        raise ValueError(f"The specified download path does not exist: {download_path}")

    # Use glob to find all CSV files in the download directory
    csv_files = [f for f in os.listdir(download_path) if f.lower().endswith('.csv')]

    return set(csv_files)
