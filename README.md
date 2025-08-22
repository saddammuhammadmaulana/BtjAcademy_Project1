## Struktur
TEST-PROJECT/
│── main.py
│── .venv/
│── .dev.env
│── .prod.env
│── readme.md
│── .gitignore

## Setup
git clone <repo-url>
cd TEST-PROJECT

python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Mac/Linux

pip install fastapi uvicorn python-dotenv


## Buat file .dev.env:

GITHUB_API=

## Jalankan Server
uvicorn main:app --reload


Docs: http://127.0.0.1:8080/docs

Redoc: http://127.0.0.1:8080/redoc

## Endpoint

GET / → Cek server

GET /items/{item_id}?q=... → Ambil item

GET /predict/ → Hitung statistik list angka

GET /distance/ → Jarak (x,y) ke (0,0)

GET /linear_regression/ → Regresi linear + prediksi

## Semua yang dipakai

FastAPI

Uvicorn

Python-dotenv

Python-statistics

Python-math