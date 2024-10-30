import os
import requests
from urllib.parse import urlparse, unquote
from tqdm import tqdm
import mimetypes

def download_file(url, dest_dir):
    # Parse the URL and extract the file name
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    filename = unquote(filename)  # Decode the URL encoding to get a readable filename
    
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)

    try:
        print(f"Attempting to download from: {url}")
        print(f"Saving to: {dest_path}")  # Debugging line
        
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Ensure we raise an error for bad responses

        # Get total file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        with open(dest_path, 'wb') as file:
            # Use tqdm to display a progress bar
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive new chunks
                        file.write(chunk)
                        bar.update(len(chunk))

        print(f"File downloaded successfully: {dest_path}")  # Confirm download success
        return dest_path  # Return the path of the downloaded file

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_copy_type(filepath):
    # Get the MIME type of a file
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type if mime_type else "unknown"

# Example usage
if __name__ == "__main__":
    test_file = "path/to/your/file.ext"  # Replace with actual file path
    print("File Type:", get_copy_type(test_file))
