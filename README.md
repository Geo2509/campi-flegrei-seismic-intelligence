# Campi Flegrei Seismic Intelligence

Open-source seismic monitoring and historical analysis project based on official INGV earthquake data.

The project analyzes approximately 30 years of seismic activity in the Campi Flegrei / Monte di Procida area using Python, Pandas and Matplotlib.

---

## Project Goals

This project aims to visualize and analyze:

- earthquake frequency
- magnitude evolution
- seismic energy release
- monthly and yearly seismic trends
- shallow earthquake activity
- earthquake depth variations
- historical seismic anomalies

The project does **not** predict earthquakes and should not be considered a civil protection or forecasting tool.

---

## Data Source

Official seismic data provided by:

- INGV — Istituto Nazionale di Geofisica e Vulcanologia
- ISIDe seismic catalog
- FDSN Event Web Service

Sources:

- https://terremoti.ingv.it/
- https://iside.rm.ingv.it/
- https://webservices.ingv.it/

All data rights belong to their respective owners.

---

## Technologies Used

- Python
- Pandas
- Matplotlib
- Requests

---

## Project Structure

```text
campi-flegrei-seismic-intelligence/
│
├── data/
│   └── earthquakes.csv
│
├── collect_earthquakes.py
├── analyze_earthquakes.py
│
├── yearly_analysis.csv
├── monthly_analysis_2020_2026.csv
├── depth_analysis_yearly.csv
│
├── earthquake_activity_yearly.png
├── max_magnitude_yearly.png
├── seismic_energy_yearly.png
│
├── earthquake_activity_monthly_2020_2026.png
├── max_magnitude_monthly_2020_2026.png
├── seismic_energy_monthly_2020_2026.png
│
├── shallow_earthquakes_yearly.png
├── avg_depth_yearly.png
│
└── README.md