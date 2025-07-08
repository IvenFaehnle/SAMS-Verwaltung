# Vollständiges Python 3.13 Image mit Debian Bullseye
FROM python:3.13-bullseye

# Arbeitsverzeichnis im Container
WORKDIR /app

# Systemabhängigkeiten installieren (wichtig für audioop & evtl. weitere Pakete)
RUN apt-get update && apt-get install -y build-essential python3-dev && rm -rf /var/lib/apt/lists/*

# Requirements kopieren und installieren
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Restlichen Code kopieren
COPY . .

# Kommando zum Starten deiner App
CMD ["python", "main.py"]

