import os
import requests
from urllib.parse import urlparse, unquote

def download_file(url, dest_dir):
    # Parse the URL and extract the file name
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename = unquote(filename)

    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)

    try:
        print(f"Attempting to download from: {url}")
        print(f"Saving to: {dest_path}")  # Debugging

        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        with open(dest_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded successfully: {dest_path}")
        return dest_path  # Return the path of the downloaded file

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
