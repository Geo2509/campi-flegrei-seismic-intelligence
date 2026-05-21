import os
import requests
import pandas as pd
from io import StringIO


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "earthquakes.csv")

os.makedirs(DATA_DIR, exist_ok=True)

URL = "https://webservices.ingv.it/fdsnws/event/1/query"

params = {
    "starttime": "1996-01-01T00:00:00",
    "endtime": "2026-12-31T23:59:59",

    # Центр примерно Monte di Procida / Campi Flegrei
    "lat": 40.798,
    "lon": 14.05,

    # Радиус поиска в километрах
    "maxradiuskm": 25,

    # Берём даже слабые события
    "minmag": 0,

    # Текстовый формат удобнее для pandas
    "format": "text",

    # Большой лимит
    "limit": 20000,

    # От старых к новым
    "orderby": "time-asc",
}

response = requests.get(URL, params=params, timeout=60)
response.raise_for_status()

text_data = response.text

df = pd.read_csv(StringIO(text_data), sep="|")

df.to_csv(OUTPUT_FILE, index=False)

print("Saved earthquakes:", len(df))
print("File:", OUTPUT_FILE)
print(df.head())