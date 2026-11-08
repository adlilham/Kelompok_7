# 📚 Simulasi Persediaan Stok Toko Buku "Cardinal"
### Aplikasi Web Simulasi Monte Carlo & Decision Support System (DSS)
**Mata Kuliah:** Teknik Simulasi dan Pemodelan  
**Teknologi:** Python 3.10+, Streamlit, NumPy, Pandas, Plotly

---

## 📌 Ringkasan Proyek
Aplikasi ini dirancang untuk memecahkan persoalan pengendalian persediaan (*inventory control*) pada **Toko Buku Cardinal**. Toko menghadapi pola permintaan harian pelanggan yang bersifat stokastik (acak) serta ketidakpastian waktu pengiriman (*lead time*) dari penerbit/distributor.

Aplikasi membantu pengambil keputusan (manajer toko) menentukan:
1. **Waktu Pemesanan Kembali (*Reorder Point / s*)**: Kapan pesanan buku baru harus dilakukan saat posisi stok menurun.
2. **Kuantitas Pemesanan (*Order Quantity / Q*)**: Berapa banyak buku yang harus dipesan setiap kali transaksi, agar risiko kehabisan stok (*stockout*) terkendali tanpa memicu pembengkakan biaya penyimpanan (*holding cost*).

---

## 🛠️ Fitur Utama Aplikasi

1. **Model Simulasi Monte Carlo Harian (s, Q)**:
   - Peninjauan stok harian dengan pembangkitan permintaan acak berdistribusi **Poisson** (diskrit) atau **Normal** (kontinu).
   - Penanganan *lost sales* ketika permintaan harian melebihi stok yang tersedia.
   - Lead time pesanan yang dapat bersifat acak seragam (min-max) atau bernilai tetap.
   - Replikasi Monte Carlo ganda ($R = 100$) untuk menghasilkan estimasi mean, deviasi standar, serta selang kepercayaan (CI 90%).

2. **Preset Kategori Judul Buku**:
   - Buku Umum (Default)
   - Novel & Fiksi
   - Buku Pelajaran
   - Buku Anak

3. **Dashboard Metrik Kinerja (KPI)**:
   - *Service Level* (% permintaan yang berhasil dipenuhi)
   - Jumlah hari kehabisan stok (*stockout days*) dan total *lost sales*
   - Rata-rata stok buku di tangan
   - Frekuensi pemesanan
   - Total biaya operasional (Biaya Simpan + Biaya Pesan + Biaya Stockout)
   - Estimasi laba bersih toko

4. **Visualisasi Interaktif (Plotly)**:
   - Grafik garis pergerakan stok harian vs Reorder Point (s) dan Safety Stock.
   - Grafik batang perbandingan permintaan vs penjualan terpenuhi vs lost sales.
   - Grafik donat komposisi biaya operasional persediaan.
   - Histogram distribusi Service Level dan Total Biaya dari seluruh replikasi.

5. **Eksperimen Perbandingan Multi-Skenario**:
   - Membandingkan 4 skenario standar persediaan (s, Q) secara serentak.
   - Fleksibilitas menambah skenario kustom melalui antarmuka formulir interaktif.
   - Grafik komparatif total biaya, laba, capaian service level, dan trade-off.

6. **Sistem Pendukung Keputusan (DSS)**:
   - Rekomendasi otomatis kombinasi (s, Q) dengan biaya terendah yang memenuhi target service level minimal (default 95%).
   - Kotak rekomendasi eksplisit dengan landasan kuantitatif dan catatan manajerial.
   - Mekanisme peringatan dan skenario terdekat jika target tidak tercapai.

7. **Ekspor Data (CSV)**:
   - Unduh log harian pergerakan stok.
   - Unduh data seluruh replikasi Monte Carlo.
   - Unduh tabel hasil perbandingan skenario.

---

## 📂 Struktur Berkas
```
Web simulasi toko barang/
│
├── app.py              # Antarmuka web interaktif Streamlit (5 Tabs utama)
├── simulation.py       # Mesin inti logika simulasi harian & Monte Carlo
├── scenarios.py        # Logika analisis multi-skenario & Decision Support System (DSS)
├── requirements.txt    # Daftar dependensi library Python
├── README.md           # Panduan instalasi dan penggunaan aplikasi
└── DOKUMENTASI.md      # Laporan teknis untuk Bab III & Bab IV tugas kuliah
```

---

## 🚀 Panduan Instalasi dan Menjalankan

### 1. Prasyarat
Pastikan komputer telah terpasang **Python 3.10** atau versi yang lebih baru.

### 2. Pasang Dependensi
Buka Terminal / Command Prompt pada direktori proyek, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
Jalankan perintah Streamlit berikut:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka pada peramban web (*browser*) di alamat `http://localhost:8501`.

---

## 📋 Struktur Tab pada Aplikasi
- **Tab 1: Beranda** — Latar belakang studi kasus, penjelasan model (s, Q), formula, dan diagram alir simulasi.
- **Tab 2: Simulasi Tunggal** — Evaluasi mendalam satu kebijakan persediaan lengkap dengan KPI cards, grafik pergerakan stok, dan log harian.
- **Tab 3: Perbandingan Skenario** — Uji coba komparatif antar kebijakan persediaan dan penambahan skenario baru.
- **Tab 4: Rekomendasi Keputusan** — Modul DSS yang merekomendasikan nilai ROP dan Order Qty terbaik berdasarkan target service level.
- **Tab 5: Data dan Unduh** — Tinjauan data mentah dan tombol ekspor ke berkas CSV.

---
Dikembangkan untuk memenuhi Tugas Mata Kuliah **Teknik Simulasi dan Pemodelan**.

