# Skadaci BK — Sistem Bimbingan & Konseling

Web application for the **Bimbingan dan Konseling (BK)** unit at **SMK Negeri 2 Cimahi**. Skadaci BK digitizes the counseling workflow so students can request counseling online, homeroom teachers and BK counselors can schedule and run sessions, and the student-affairs office (kesiswaan) can keep structured reports and violation records.

> **Tugas Akhir (Final Project)** — Developer: **Andhika Andriana Putra** (XI RPL A).

**Live**: https://bksmkn2cimahi.vercel.app

## Stack

- **Python 3** + **Flask** (routing, templating, sessions)
- **MySQL** (data persistence, schema in `instance/db_bk_dhika.sql`)
- **Jinja2** server-rendered HTML templates
- **Vanilla HTML / CSS / JavaScript** on the front end
- **FPDF** for PDF report generation
- **Werkzeug** security helpers (password hashing)
- **Gunicorn** as the production WSGI server
- **Vercel** for hosting (serverless entrypoint: `api/index.py`)

## Features

- **Multi-role authentication** — separate dashboards and permission scopes for:
  - **Siswa** (student) — request counseling, view history, update profile
  - **Guru BK** (counselor) — manage counseling sessions, complaints, parent calls
  - **Wali Kelas** (homeroom teacher) — review student records
  - **Kesiswaan** (student affairs) — violation records, reports
  - **Admin** — full access
- **Konseling online** — students submit counseling requests; counselors schedule, run, and close sessions
- **Pelanggaran** — violation tracking with photo evidence uploads
- **Pemanggilan orang tua** — parent-call records
- **Pengaduan** — complaint workflow
- **Chat internal** — in-app messaging between roles
- **Laporan** — printable PDF reports per category
- **Upload** — profile photos and violation evidence (jpg/jpeg/png/webp, 5 MB cap)
- **Pagination, hashing, and password verification** — all server-side

## Project structure

```
appBK_dhika.py        # main Flask app (routes, models, auth, helpers)
api/
  index.py            # Vercel serverless entrypoint
dikatools.sh          # dev / deploy helper
requirements.txt
instance/
  db_bk_dhika.sql     # MySQL schema + seed
static/               # CSS, JS, uploads
templates/
  base_dhika.html
  auth/               login
  dashboard/          per-role dashboards
  data/               list views
  detail/             detail views
  guru/               counselor views
  konseling/          counseling flow
  laporan/            reports
  akun/               profile
  chat_dhika.html
  pagination_dhika.html
  404_dhika.html
docs/
  AndhikaAP_KonsepTA.docx
  AndhikaAP_KonsepTA_TugasPJJ.docx
```

## Local development

```bash
# 1. Create a virtualenv and install dependencies
python -m venv .venv
. .venv/Scripts/activate      # Windows
pip install -r requirements.txt

# 2. Import the database schema
mysql -u root -p < instance/db_bk_dhika.sql

# 3. Run the dev server
python appBK_dhika.py
# or, via the deploy helper:
bash dikatools.sh
```

The app listens on `http://127.0.0.1:5000` by default.

## Deployment

The repo is configured for **Vercel** as a serverless Python app. The `api/index.py` entrypoint re-exports the Flask `app` object defined in `appBK_dhika.py`. Set the MySQL connection details as Vercel environment variables before deploying.

## License

All rights reserved. Source code is published as a final-project archive; please contact the author before reuse.
