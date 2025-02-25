# Snelnotuleren Python SDK
[![PyPI version](https://badge.fury.io/py/snelnotuleren-sdk.svg)](https://badge.fury.io/py/snelnotuleren-sdk)
[![Python versions](https://img.shields.io/pypi/pyversions/snelnotuleren-sdk.svg)](https://pypi.org/project/snelnotuleren-sdk/)

Python SDK voor de Snelnotuleren.nl API. Automatiseer het verwerken van audio-opnames naar notulen.

## Installatie

```bash
pip install snelnotuleren-sdk
```

## Gebruik

### API Credentials aanmaken
Je kunt op twee manieren API credentials krijgen:

1. Via het dashboard op [dashboard.snelnotuleren.nl](https://dashboard.snelnotuleren.nl)
2. Programmatisch via de SDK:

```python
from snelnotuleren import SnelNotulerenClient

# Maak nieuwe credentials aan
client = SnelNotulerenClient()
credentials = client.create_client_credentials(
    label="Mijn API Client",
    description="Voor automatische verwerking"
)

print(f"Client ID: {credentials['client_id']}")
print(f"Client Secret: {credentials['client_secret']}")
print(f"Webhook Secret: {credentials['webhook_secret']}")  # Voor webhook verificatie
```

### Notulen verwerken

```python
from snelnotuleren import SnelNotulerenClient

# Initialiseer met je credentials
client = SnelNotulerenClient(
    client_id='jouw_client_id',
    client_secret='jouw_client_secret'
)

# Basis gebruik met verplichte velden
order_id = client.create_order(
    file_path='vergadering.mp3', # Verplicht, 
    email='contact@bedrijf.nl', # Verplicht, 
    context='Maandelijkse vergadering', # Verplicht, 
    meeting_date='2025-02-23',  # Verplicht, format: YYYY-MM-DD
    smart_detection=True,       # Verplicht, voor automatische agendapunt detectie
    report_type='middel_notulen',  # Optional, standaard op 'transcriptie'
    webhook_url='https://jouw-domein.nl/webhook'
)

# Met unstructured_agenda
order_id = client.create_order(
    file_path='vergadering.mp3',
    email='contact@bedrijf.nl',
    context='Maandelijkse vergadering',
    meeting_date='2025-02-23',
    unstructured_agenda='1.opening, 2. medelingen. (3) financien, 3.a omzet, etc...' # Hier is geen format verplicht, LLM herkent agendapunten
    webhook_url='https://jouw-domein.nl/webhook'
)

# Met experimentele features
order_id = client.create_order(
    file_path='vergadering.mp3',
    email='contact@bedrijf.nl',
    context='Maandelijkse vergadering',
    meeting_date='2025-02-23',
    smart_detection=True,
    # Experimentele features
    speaker_diarization=True,  # Optioneel, experimenteel
    speaker_count=4,          # Optioneel, experimenteel (1-10)
    speaker_names=['Jan', 'Piet', 'Marie', 'Anna'],  # Optioneel, experimenteel
    webhook_url='https://jouw-domein.nl/webhook'
)
```

Implementeer een webhook handler:

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verifieer de webhook signature
    signature = request.headers.get('X-Webhook-Signature')
    payload = request.get_data().decode('utf-8')
    
    expected_signature = hmac.new(
        'jouw_webhook_secret'.encode(),  # Van je credentials
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected_signature:
        return 'Invalid signature', 401

    # Verwerk de webhook
    data = request.json
    
    if data['event'] == 'processing.completed':
        # Notulen zijn klaar
        notulen = data['data']['notulen']
        print(f"✅ Notulen ontvangen voor order {data['order_id']}")
        
    elif data['event'] == 'processing.failed':
        print(f"❌ Error voor order {data['order_id']}: {data['error']}")
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=8080)
```

## Parameters

- `file_path`: Pad naar het audio bestand
- `email`: Email adres voor notificaties
- `context`: Naam/context van de vergadering
- `meeting_date`: Datum van de vergadering (format: YYYY-MM-DD)
- `smart_detection`: Automatische agendapunt detectie (boolean)
- `webhook_url`: URL voor webhook notificaties
- `report_type`: Type rapport (default: 'transcriptie')
- `unstructured_agenda`: Ongestructureerde agenda tekst

## Experimentele Features

De volgende features zijn in beta en kunnen wijzigen:

- `speaker_diarization`: Sprekerherkenning gebruiken (boolean)
- `speaker_count`: Verwacht aantal sprekers (1-10)
- `speaker_names`: Lijst met namen van sprekers

## Report Types

- `transcriptie`: Alleen transcriptie (€5)
- `korte_notulen`: Beknopte notulen (€10)
- `middel_notulen`: Uitgebreide notulen (€20)
- `lange_notulen`: Complete notulen met details (€25)

## Webhook Events

Je kunt deze events verwachten:

- `processing.completed`: Notulen zijn succesvol verwerkt
  ```json
  {
    "event": "processing.completed",
    "order_id": "order_123",
    "status": "completed",
    "data": {
      "meeting_name": "Maandelijkse vergadering",
      "meeting_date": "2024-02-22",
      "notulen": "1. Opening\nDe vergadering wordt geopend... 2. Rondvraag\nEr werd...",
      "speakers": ["Spreker 1", "Spreker 2"],
      "metadata": {
        "speaker_diarization": true,
        "speakers_expected": 2,
        "detected_language": "nl",
        "categories": ["Opening", "Rondvraag"]
      }
    }
  }
  ```

- `processing.failed`: Er is een fout opgetreden
  ```json
  {
    "event": "processing.failed",
    "order_id": "order_123",
    "status": "failed",
    "error": "Beschrijving van de fout"
  }
  ```

## Security Best Practices

1. Bewaar je client secret en webhook secret veilig
2. Verifieer altijd de webhook signature
3. Gebruik HTTPS voor je webhook endpoint
4. Implementeer rate limiting op je webhook endpoint