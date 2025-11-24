# Medical Codex Pipeline

This project contains Python-based ETL pipelines for processing and standardizing
major medical codex datasets used in healthcare systems.

## ✅ Currently Implemented Codexes

- ICD-10 (WHO) – International disease classification codes

## 📁 Project Structure

```
medical-codex-pipeline/

├── input/ # Raw data files (excluded from Git)

├── scripts/ # ETL processing scripts

├── output/csv/ # Clean standardized CSV outputs

├── utils/ # Shared utility functions

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

## ▶️ Running the ICD-10 Pipeline

Place your ICD-10 file in:

```
input/icd10who_codes_2024.csv
```

Must contain columns:

- Code
- Description

Then run:

```bash
python scripts/icd10who_processor.py
```

Output appears here:

```
output/csv/icd10who_clean.csv
```

## 📦 Output Format

All codexes are standardized to:

- code
- description
- last_updated

Example:

```
code,description,last_updated
A00,Cholera,2025-01-01 12:00:00
```

## 🧠 Technologies

- Python 3.9+
- pandas
- logging
- pathlib

## 🚀 Next Steps

- Add SNOMED, LOINC, RxNorm, NPI, HCPCS
- Add automated downloads
- Add GitHub Actions
