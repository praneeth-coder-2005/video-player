import os
import requests
from urllib.parse import urlparse, unquote
from tqdm import tqdm
import psutil  # For system performance information

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

        total_size = int(response.headers.get('content-length', 0))
        with open(dest_path, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, 
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]") as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        bar.update(len(chunk))

                        # Show system performance stats
                        cpu_percent = psutil.cpu_percent()
                        ram_info = psutil.virtual_memory()
                        free_ram = ram_info.available / (1024 * 1024)  # Convert to MB
                        processed_mb = file.tell() / (1024 * 1024)  # Current size written in MB
                        total_size_mb = total_size / (1024 * 1024)  # Convert to MB
                        speed = len(chunk) / 1024.0  # Speed in KB

                        print(f"├ Progress: {bar.n / total_size * 100:.2f}%")
                        print(f"├ Processed: {processed_mb:.2f}MB")
                        print(f"├ Total Size: {total_size_mb:.2f}MB")
                        print(f"├ Speed: {speed:.2f}KB/s")
                        print(f"├ CPU: {cpu_percent}% | RAM: {ram_info.percent}% | FREE: {free_ram:.2f}MB")

        print(f"File downloaded successfully: {dest_path}")
        return dest_path

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
