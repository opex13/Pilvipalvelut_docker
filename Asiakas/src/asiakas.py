import os
import requests
import time
import hashlib

# Environment variables
palvelimen_osoite = os.getenv('SERVER_ADDRESS', 'http://palvelin:8000')
dataa_kansio = os.getenv('DATA_DIR', 'dataa')
log_file = f"{dataa_kansio}/log.txt"

def calculate_checksum(file_path):
    """Calculate SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def log_message(message):
    """Log a message with a timestamp."""
    with open(log_file, 'a') as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        print(message)

def run():
    os.makedirs(dataa_kansio, exist_ok=True)
    file_path = f"{dataa_kansio}/tiedosto_palvelimelta.txt"

    while True:
        try:
            # Fetch the file
            file_response = requests.get(f"{palvelimen_osoite}/file", stream=True)
            if file_response.status_code == 200:
                # Save the file locally
                with open(file_path, 'wb') as f:
                    for chunk in file_response.iter_content(chunk_size=1024):
                        f.write(chunk)
                log_message("File downloaded successfully.")

                # Fetch the server's checksum
                checksum_response = requests.get(f"{palvelimen_osoite}/checksum")
                if checksum_response.status_code == 200:
                    server_checksum = checksum_response.text.strip()

                    # Calculate the checksum of the downloaded file
                    local_checksum = calculate_checksum(file_path)

                    # Compare checksums
                    if local_checksum == server_checksum:
                        log_message(f"Checksum verified: {local_checksum}")
                    else:
                        log_message(f"Checksum mismatch! Local: {local_checksum}, Server: {server_checksum}")
                else:
                    log_message("Failed to fetch server checksum.")
            else:
                log_message(f"Failed to download file. Server responded with status: {file_response.status_code}")

        except requests.exceptions.RequestException as e:
            log_message(f"Connection error: {e}")

        # Wait before the next iteration
        time.sleep(60)

if __name__ == "__main__":
    run()
