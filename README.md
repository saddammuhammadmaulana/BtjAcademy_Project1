# 🚀 TEST-PROJECT  

Project ini adalah contoh **FastAPI sederhana** dengan beberapa endpoint untuk perhitungan matematika dan statistik.  
Didesain simpel agar mudah dipelajari, cocok buat pemula yang ingin coba bikin REST API.

---

## 📂 Struktur Project
TEST-PROJECT/
│── main.py
│── .venv/
│── .dev.env
│── .prod.env
│── readme.md
│── .gitignore

yaml
Copy
Edit

---

## ⚙️ Setup Project

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd TEST-PROJECT
Buat Virtual Environment

bash
Copy
Edit
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python -m venv .venv
source .venv/bin/activate
Install Dependencies

bash
Copy
Edit
pip install fastapi uvicorn python-dotenv
 Buat file .dev.env
Isi dengan token/API key yang dibutuhkan:

makefile
Copy
Edit
GITHUB_API=
▶Jalankan Server
bash
Copy
Edit
uvicorn main:app --reload
Swagger Docs → http://127.0.0.1:8080/docs

Redoc → http://127.0.0.1:8080/redoc

Endpoint yang Tersedia
GET / → Cek server

GET /items/{item_id}?q=... → Ambil item berdasarkan ID + query opsional

GET /predict/ → Hitung statistik dari list angka

GET /distance/ → Hitung jarak (x,y) ke titik (0,0)

GET /linear_regression/ → Regresi linear + prediksi

Teknologi yang Digunakan
FastAPI 

Uvicorn 

python-dotenv 

Built-in: statistics, math