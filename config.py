import os
import requests
from urllib.parse import urlparse, unquote

def download_file(url, dest_dir):
    # Parse the URL and extract the file name
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename = unquote(filename)  # Decode the URL encoding to get a readable filename

    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)

    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure we raise an error if the download failed
    with open(dest_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    return dest_path
