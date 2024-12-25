# Skriptit:
## Palvelimen käynnistys .sh skriptilla:
```bash
#!/bin/bash

# Luodaan tarvittavat volyymit
docker volume create servervol

# Luodaan verkko
docker network create verkko

# Käynnistetään palvelimen kontti
docker build -t palvelin ./Palvelin
docker run -d --name palvelin \
  --network verkko \
  -v servervol:/serverdata \
  -e DATA_DIR=/serverdata \
  -e PORT=8000 \
  -e PYTHONUNBUFFERED=1 \
  -p 8000:8000 \
  palvelin

echo "Palvelin kontti on käynnistetty ja verkko 'verkko' on luotu."
```
## Palvelimen pysäytys .sh skriptilla:

```bash
#!/bin/bash

# pysäytetään palvelin kontti
docker stop palvelin

# poistetaan the palvelin kontti
docker rm palvelin
docker volume rm servervol

echo "Palvelin kontti on pysäytetty ja poistettu."
```

## Asiakkaan käynntistys .sh skriptilla:

```bash
#!/bin/bash

# Luodaan tarvittavat volyymit
docker volume create clientvol

# Luodaan verkko
docker network create verkko

# Käynnistetään asiakkaan kontti
docker build -t asiakas ./Asiakas
docker run -d --name asiakas \
  --network verkko \
  -v clientvol:/clientdata \
  -e DATA_DIR=/clientdata \
  -e SERVER_ADDRESS=http://palvelin:8000 \
  -e PYTHONUNBUFFERED=1 \
  asiakas

echo "Asiakas kontti on käynnistetty ja verkko 'verkko' on luotu."
```

## Asiakkaan pysäytys .sh skriptilla:

```bash
#!/bin/bash

# pysäytettään asiakas kontti
docker stop asiakas

# poistetaan the asiakas kontti
docker rm asiakas

echo "Asiakas kontti on pysäytetty ja poistettu."

docker volume rm clientvol

# poistetaan the verkko
docker network rm verkko

echo "Verkko ja volyymit on poistettu."
```

## Shell skriptille pitää muistaa antaa suoritusoikeus:
```bash
chmod +x stop_palvelin.sh
chmod +x stop_asiakas.sh
```