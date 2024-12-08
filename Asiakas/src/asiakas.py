import os
import requests

palvelimen_osoite = os.getenv('SERVER_ADDRESS', 'http://palvelin:8000')
dataa_kansio = "asiakasdataa"

def run():
    os.makedirs(dataa_kansio, exist_ok=True)
    
    vastaus = requests.get(palvelimen_osoite)
    if vastaus.status_code == 200:
            
        with open(f"{dataa_kansio}/tiedosto_palvelimelta.txt", 'w') as f:
            f.write(vastaus.text)
        print("Tiedosto on vastaanotettu ja tallennetu kohteeseen kansio/tiedosto ")
    else:
        print("metsään meni.")

if __name__ == "__main__":
    run()