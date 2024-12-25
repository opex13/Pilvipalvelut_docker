import os
import random
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer

port = int(os.getenv('PORT', 8000))
kansio_data = os.getenv('DATA_DIR', 'dataa')

def generate_file_and_checksum(tiedosto):
    #Generate a random text file and return its checksum.
    os.makedirs(os.path.dirname(tiedosto), exist_ok=True)
    with open(tiedosto, "w") as f:
        satunnainenTeksti = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=1024))
        f.write(satunnainenTeksti)
    with open(tiedosto, 'rb') as f:
        checksum = hashlib.sha256(f.read()).hexdigest()
    return checksum

class PalvelinApp(BaseHTTPRequestHandler):
    def do_GET(self):
        tiedosto = f"{kansio_data}/data.txt"

        # Ensure the file and checksum exist
        if not os.path.exists(tiedosto):
            checksum = generate_file_and_checksum(tiedosto)

        # Serve the file
        if self.path == '/file':
            if os.path.exists(tiedosto):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(tiedosto)}"')
                self.end_headers()
                with open(tiedosto, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
        
        # Serve the checksum
        elif self.path == '/checksum':
            if os.path.exists(tiedosto):
                with open(tiedosto, 'rb') as f:
                    checksum = hashlib.sha256(f.read()).hexdigest()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(checksum.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Checksum not available")
        
        # Default: Indicate server is ready
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Server is ready and file generation is automatic.")

def run():
    os.makedirs(kansio_data, exist_ok=True)
    palvelin = HTTPServer(('0.0.0.0', port), PalvelinApp)
    print(f"Server running on port {port}")
    palvelin.serve_forever()

if __name__ == "__main__":
    run()
