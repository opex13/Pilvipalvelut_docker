import os
import random
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer

port = int(os.getenv('PORT', 8000))

kansio_data = "dataa"

class PalvelinApp(BaseHTTPRequestHandler):
    def do_GET(self):
        
        #luodaan tiedosto
        tiedosto = f"{kansio_data}/data.txt"
        with open(tiedosto, "w") as f:
            satunnainenTeksti = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=1024))
            f.write(satunnainenTeksti)
            
        #tarkistussumman laskenta
        with open(tiedosto, 'rb') as f:
            tarkistussumma = hashlib.sha256(f.read()).hexdigest()
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"tiedosto: {tiedosto}\nTarksitussumma: {tarkistussumma}".encode())
        
def run():
    os.makedirs(kansio_data, exist_ok=True)
    palvelin = HTTPServer(('0.0.0.0', port), PalvelinApp)
    print(f"Palvelin käynnissä portilla {port}")
    palvelin.serve_forever()
    
if __name__ == "__main__":
    run()
        