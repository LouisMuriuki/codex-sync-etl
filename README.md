# Medical Codex Pipeline

Production-style ETL pipelines for processing and standardizing major medical codex datasets used in healthcare systems.

## ✅ Currently Implemented Codexes

- ICD-10 (WHO) – International disease classification codes
- ICD-10-CM (US) – Diagnosis codes
- NPI (US) – National Provider Identifier registry

## 📁 Project Structure

```
medical-codex-pipeline/

├── input/              # Raw data files (excluded from Git)
├── scripts/            # ETL processing scripts
│   ├── icd10who_processor.py
│   └── npi_processor.py
├── output/
│   └── csv/            # Clean standardized CSV outputs
├── utils/              # Shared utility functions
├── requirements.txt
└── README.md
```

## ⚙️ Setup

```bash
git clone <your-repo>
cd medical-codex-pipeline
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## ▶️ Run: ICD-10 (WHO)

Place your ICD-10 file at:

```
input/icd10who_codes_2024.csv
```

Required columns:
- Code
- Description

Run:

```bash
python scripts/icd10who_processor.py
```

Output:
```
output/csv/icd10who_clean.csv
```

Optional: download via env var
```bash
export ICD10WHO_URL="https://example.com/icd10who_codes_2024.csv"
python scripts/icd10who_processor.py
```

## ▶️ Run: NPI (US)

Place your NPI file at:
```
input/npi_registry.csv
```

Minimum columns (the script adapts to common NPPES headers):
- NPI
- One of:
  - Provider Organization Name (Legal Business Name)
  - Provider Last Name (Legal Name) + Provider First Name

Run:
```bash
python scripts/npi_processor.py
```

Output:
```
output/csv/npi_clean.csv
```

Optional: download via env var
```bash
export NPI_URL="https://example.com/npi_registry.csv"
python scripts/npi_processor.py
```

## ▶️ Run: ICD-10-CM (US)

Place your ICD-10-CM file at:
```
input/icd10cm_codes_2024.txt
```

Expected columns (flexible):
- Code
- One of:
  - Long Description
  - Description
  - Short Description

Run:
```bash
python scripts/icd10cm_processor.py
```

Output:
```
output/csv/icd10cm_clean.csv
```

Optional: download via env var
```bash
export ICD10CM_URL="https://example.com/icd10cm_codes_2024.txt"
python scripts/icd10cm_processor.py
```

## 📦 Standardized Output Schema

All codex outputs use:
- code
- description
- last_updated

Example:
```
code,description,last_updated
A00,Cholera,2025-01-01 12:00:00
```

## 🧠 Tech Stack

- Python 3.9+
- pandas
- requests
- logging
- pathlib

## 🚀 Roadmap

- Add SNOMED, LOINC, RxNorm, HCPCS processors
- Optional web downloads for all codexes
- GitHub Actions for scheduled refresh and validation
