# Pilvipalvelut_docker

Tämä projekti esittelee tiedoston synkronointijärjestelmän, joka käyttää Docker Composea. Järjestelmä koostuu kahdesta pyhton ohjelmista: `palvelin` (server) ja `asiakas` (client). `Palvelin` luo satunnaisen tiedoston ja tarjoaa sen sekä tarkistussumman HTTP:n kautta. `Asiakas` hakee tiedoston ja varmistaa sen eheyden tarkistamalla tarkistussumman.

## Projektin rakenne
```.
├── docker-compose.yml  # Määrittelee palvelut, volyymit ja verkon 
├── Palvelin/           # Palvelimen tiedostot 
│ └── Palvelin.py       # Palvelimen koodi 
├── Asiakas/            # Asiakkaan tiedostot 
│ └── Asiakas.py        # Asiakkaan koodi
```
## Ominaisuudet

- **Palvelin (`palvelin.py`)**:
  - Luo satunnaisen tiedoston ja laskee sen tarkistussumman.
  - Tarjoaa endpointit tiedoston lataamiseen (`/file`) ja tarkistussumman hakemiseen (`/checksum`).

- **Asiakas (`asiakas.py`)**:
  - Lataa tiedoston palvelimelta 60 sekunnin välein.
  - Varmistaa tiedoston eheyden vertaamalla tarkistussummat.
  - Kirjaa prosessin lokiin ja raportoi mahdolliset ongelmat.

## Vaatimukset

- Asennettu Docker ja Docker Compose.

## Asennus ja käyttö

1. Kloonaa tämä repositorio:
   ```bash
   git clone https://github.com/opex13/Pilvipalvelut_docker.git
   cd Pilvipalvelut_docker
2. Rakenna ja käynnistä palvelut:
   ```bash
   docker-compose up --build
3. Palvelut käynnistyvät:

- palvelin käynnistyy portissa 8000 ja luo tiedoston automaattisesti.
- asiakas hakee tiedoston 60 sekunnin välein, varmistaa tarkistussumman ja kirjaa tulokset lokiin.
4. Näytä asiakas-palvelun lokit:
```bash
docker logs asiakas
```
## Endpointit
- Palvelimen endpointit (`palvelin.py`):
-- `/file`: Lataa luotu tiedosto.
-- `/checksum`: Hae tiedoston tarkistussumma.

## Ympäristömuuttujat
Palvelut käyttävät ympäristömuuttujia konfigurointiin:

### Palvelin (palvelin):
- `DATA_DIR`: Hakemisto, johon luotu tiedosto tallennetaan (oletus: `dataa`).
- `PORT`: HTTP-palvelimen portti (oletus: `8000`).
### Asiakas (asiakas):
- `DATA_DIR`: Hakemisto, johon ladattu tiedosto tallennetaan (oletus: `dataa`).
- `SERVER_ADDRESS`: Palvelimen osoite (oletus: `http://palvelin:8000`).
## Lokit
- Asiakas-palvelu kirjoittaa lokit log.txt-tiedostoon hakemistossa `DATA_DIR`. Lokit sisältävät:

- Tiedoston latauksen onnistumiset/epäonnistumiset.
- Tarkistussumman varmistustulokset.
- Yhteysongelmat.
### Esimerkki lokeista:
```
2024-12-25 14:00:00 - Tiedosto ladattiin onnistuneesti.
2024-12-25 14:00:01 - Tarkistussumma varmennettu: d7c7b6b9a1f5b36e3a3e7f9e987d8b6e7c7f4b9e6b8c6a1
2024-12-25 14:01:00 - Tiedosto ladattiin onnistuneesti.
2024-12-25 14:01:01 - Tarkistussumma ei täsmää! Paikallinen: abc123, Palvelin: d7c7b6...
```

## Verkko ja volyymit
### Verkko: Palvelut kommunikoivat `verkko`-nimisessa verkossa.
### Volyymit:
- `servervol`: Tallentaa palvelimen luomat tiedostot.
- `clientvol`: Tallentaa asiakkaan lataamat tiedostot ja lokit.
## Palveluiden pysäyttäminen
- Pysäytä palvelut komennolla:
```
docker-compose down
```
- Pysäytä palvelut poistamalla väliaikaiset tiedostot:
```
docker-compose down -v
```