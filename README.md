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
## 📊 Data Jaringan Jalan (GeoJSON)

File **`Jaringan_jalanan_indonesia.geojson`** tidak disertakan dalam repo karena ukurannya melebihi batas GitHub (>100 MB).  

➡️ Kamu bisa **mengunduh data shapefile jaringan jalan (SHP)** dari situs berikut:  
👉 [Download Shapefile Jaringan Jalan Indonesia](https://www.indonesia-geospasial.com/2024/12/download-shapefile-jaringan-jalan.html)  

Setelah diunduh, kamu bisa mengonversi SHP menjadi GeoJSON dengan tools seperti:  
- [QGIS](https://qgis.org/)  
- [GDAL/ogr2ogr](https://gdal.org/programs/ogr2ogr.html)  
- Python `geopandas`  

---

## 🔧 Teknologi yang Digunakan
- [Streamlit](https://streamlit.io/)  
- [Pandas](https://pandas.pydata.org/)  
- [Folium](https://python-visualization.github.io/folium/)  
- [GeoJSON](https://geojson.org/)  
- Algoritma **Dijkstra** untuk rute terdekat  

---
