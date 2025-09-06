# 🗺️ Rute Bidan Jakarta

Aplikasi berbasis **Streamlit** untuk menampilkan rute terdekat menuju bidan di Jakarta menggunakan data jaringan jalan dalam format **GeoJSON**.  
Aplikasi ini meniru fungsi sederhana seperti **Google Maps**, tapi fokus pada layanan bidan dengan rute terdekat.

---

## 🚀 Fitur
- Input lokasi pengguna (manual latitude/longitude, bisa dikembangkan dengan geolokasi browser).  
- Pilih tujuan **bidan** dari CSV (`bidan_points.csv`).  
- Hitung rute terdekat menggunakan **algoritma Dijkstra**.  
- Visualisasi peta interaktif dengan **Folium**:
  - Marker posisi pengguna (biru).
  - Marker bidan tujuan (merah).
  - Garis rute (hijau).
- Optimasi performa:
  - **Filter data** hanya wilayah Jakarta dari GeoJSON besar.
  - **`st.session_state`** untuk caching graph, data bidan, dan rute agar tidak terus-ter-refresh.

---

## 📸 Screenshot
Contoh tampilan aplikasi di browser:

![Contoh Peta Rute](images/image.png)

> Letakkan screenshot aplikasi kamu di folder `images/` dengan nama `screenshot.png`.

---

## 📂 Struktur Folder
.
├── app.py
├── bidan_points.csv
├── Jaringan_jalanan_indonesia.geojson # Tidak disimpan di GitHub (karena >100 MB)
├── requirements.txt
└── images/
└── screenshot.png

yaml
Salin kode

---

## ⚙️ Instalasi & Menjalankan

1. Clone repository:
   ```bash
   git clone https://github.com/username/repo-rute-bidan.git
   cd repo-rute-bidan
Install dependencies:

bash
Salin kode
pip install -r requirements.txt
Jalankan aplikasi:

bash
Salin kode
streamlit run app.py
Buka browser ke: http://localhost:8501

📊 Data Jaringan Jalan (GeoJSON)
File Jaringan_jalanan_indonesia.geojson tidak disertakan dalam repo karena ukurannya melebihi batas GitHub (>100 MB).

Kamu bisa mengunduh data shapefile jaringan jalan (dengan format SHP) dari situs Indonesia-Geospasial:
👉 Download Shapefile Jaringan Jalan Indonesia 
INDONESIA GEOSPASIAL

Setelah diunduh, kamu bisa mengonversi SHP menjadi GeoJSON dengan tools seperti ogr2ogr, geopandas, atau QGIS.

🔧 Teknologi yang Digunakan
Streamlit

Pandas

Folium

GeoJSON

Algoritma Dijkstra untuk rute terdekat# Rute-Bidan
