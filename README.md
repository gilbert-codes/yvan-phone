# Yvan Phone Store (Django)

Simple Django project to manage phones, images, prices, descriptions and voice notes.

Getting started (Windows):

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Copy the example `.env` and fill secrets locally (do NOT commit `.env`):

```powershell
copy .env.example .env
# edit .env and fill GOOGLE_MAPS_API_KEY and SECRET_KEY
```

3. Install requirements:

```powershell
pip install -r requirements.txt
```

4. Apply migrations and create superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```powershell
python manage.py runserver
```

5. Open admin at `http://127.0.0.1:8000/admin/` to add categories and phones. Upload images and optional audio files.

Notes:
- Media files are stored in the `media/` folder. Ensure `MEDIA_ROOT` is writable.
- The phone detail page can generate a voice MP3 from the phone description using gTTS (press the Generate button). The generated MP3 will be saved under `media/voice/`.
- Categories you mentioned: Google Pixel (3-10), iPhone (X-17 Pro Max), Samsung Galaxy A and S, Sony (Mac?) 2-5, Aquas 6-8, Tecno, Kiosera, Accessories.

Map embedding:
- To show an embedded Google Map under each phone's description, set `STORE_LAT` and `STORE_LON` environment variables (latitude and longitude).
- Example (PowerShell):

```powershell
$env:STORE_LAT = '-26.2041'
$env:STORE_LON = '28.0473'
$env:STORE_NAME = 'Yvan Phone Store'
```

To use the Google Maps JavaScript API for a richer interactive map, set a `GOOGLE_MAPS_API_KEY` environment variable with your API key and enable the Maps JavaScript API in the Google Cloud Console. Example (PowerShell):

```powershell
$env:GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY'
```

If `GOOGLE_MAPS_API_KEY` is set, the detail page will load the Maps JavaScript API and show an interactive map with a marker. If not, the page falls back to the simple iframe embed.
