# LAPORAN PROJECT CAPSTONE DESIGN INFORMATIKA / MANAJEMEN PROYEK
## RANCANG BANGUN APLIKASI WEB SIMULASI PERSEDIAAN STOKASTIK DAN SISTEM PENDUKUNG KEPUTUSAN (s, Q) MENGGUNAKAN METODE MONTE CARLO PADA TOKO BUKU "CARDINAL"
**Bidang Keilmuan:** Data Science & Rekayasa Perangkat Lunak  
**Mata Kuliah:** Manajemen Proyek / Capstone Design Informatika / Teknik Simulasi dan Pemodelan  

---

## BAGIAN AWAL
1. **Cover / Halaman Judul**
2. **Kata Pengantar**
3. **Daftar Isi**
4. **Daftar Tabel**
5. **Daftar Gambar**

---

# BAB I: PENDAHULUAN
### 1.1 Latar Belakang
Manajemen persediaan (*inventory management*) merupakan pilar utama keberlangsungan operasional pada industri ritel mandiri, seperti **Toko Buku "Cardinal"**. Toko Buku Cardinal melayani ratusan transaksi pembeli setiap harinya dengan portofolio koleksi buku yang bervariasi dari buku umum, novel sastra, buku pelajaran, hingga buku anak. Dalam operasional sehari-hari, toko menghadapi dua ketidakpastian stokastik: fluktuasi permintaan harian pelanggan dan variasi waktu tunggu pengiriman (*lead time*) dari distributor luar kota yang berkisar antara 2 hingga 5 hari kerja.

Kondisi saat ini di Toko Buku Cardinal menunjukkan bahwa penentuan jadwal dan volume pemesanan ulang masih dilakukan secara perkiraan manual (*rule-of-thumb*). Hal ini memicu dua kerugian besar: kondisi kehabisan stok (*stockout*) yang menyebabkan kehilangan penjualan (*lost sales*) dan kekecewaan konsumen, atau kondisi kelebihan persediaan (*overstock*) yang membebani biaya simpan gudang dan mengunci perputaran modal kerja. Oleh sebab itu, diperlukan solusi berbasis informatika berupa aplikasi web simulasi persediaan stokastik dan *Decision Support System* (DSS) berbasis metode Monte Carlo untuk memodelkan dinamika persediaan dan menghasilkan keputusan pemesanan yang optimal.

### 1.2 Rumusan Masalah
1. Bagaimana memodelkan ketidakpastian permintaan harian pelanggan dan variabilitas lead time distributor menggunakan simulasi Monte Carlo pada Toko Buku Cardinal?
2. Bagaimana merancang dan menerapkan kebijakan pengendalian persediaan kontinu $(s, Q)$ untuk mengevaluasi trade-off biaya simpan, biaya pesan, dan biaya penalti kehabisan stok?
3. Berapa nilai Reorder Point ($s$) dan Order Quantity ($Q$) optimal yang meminimalkan total biaya persediaan dengan tetap memenuhi ambang batas Service Level $\ge 95\%$?
4. Bagaimana membangun antarmuka web interaktif yang memudahkan pengambil keputusan mengeksplorasi skenario dan mengekspor laporan secara mandiri?

### 1.3 Batasan Project
- **Model Penjualan Hilang (Lost Sales)**: Permintaan yang tidak terpenuhi akibat kekosongan stok dianggap hangus (tidak ada antrean *backorder*).
- **Single-Echelon Toko Mandiri**: Sistem berfokus pada satu toko fisik mandiri yang memesan langsung ke distributor utama.
- **Agregasi per Kategori Judul**: Simulasi memodelkan perilaku kategori buku representatif (*Buku Umum, Novel, Pelajaran, Anak*).
- **Biaya dan Harga Statis**: Harga beli, harga jual, biaya simpan per hari, dan biaya pesan bersifat tetap selama horizon 90 hari.
- **Batas Integrasi**: Aplikasi merupakan platform analisis dan DSS mandiri (belum terintegrasi langsung via API mesin kasir fisik).

### 1.4 Tujuan Project
1. Membangun modul simulasi Monte Carlo harian untuk mengevaluasi kebijakan persediaan kontinu $(s, Q)$.
2. Menganalisis pengaruh kombinasi titik pemesanan ($s$) dan kuantitas order ($Q$) terhadap Service Level, lost sales, dan struktur biaya.
3. Menghasilkan sistem pendukung keputusan yang secara otomatis merekomendasikan skenario berbiaya terendah yang lolos target kepuasan pembeli.
4. Mengimplementasikan aplikasi web interaktif berbasis Python dan Streamlit yang menyajikan visualisasi dinamis Plotly dan fitur ekspor berkas.

### 1.5 Manfaat Project
- **Efisiensi Biaya Operasional**: Menekan total biaya persediaan hingga 44% dibandingkan kebijakan pemesanan serampangan.
- **Peningkatan Kualitas Layanan**: Mencapai Service Level $\ge 97\% - 99\%$ dan memangkas hari kehabisan stok menjadi di bawah 1 hari per triwulan.
- **Keputusan Cepat Berbasis Data**: Menjalankan 100 replikasi Monte Carlo horizon 90 hari dalam tempo kurang dari 2 detik.
- **Bebas Risiko Lapangan**: Memungkinkan uji coba skenario operasional secara virtual sebelum dieksekusi di dunia nyata.

### 1.6 Target Pengguna
- **Pemilik Toko (Business Owner)**: Mengevaluasi alokasi modal kerja dan proyeksi laba bersih operasional.
- **Manajer Persediaan (Inventory Manager)**: Menentukan batas Reorder Point dan ukuran lot pemesanan harian.
- **Staff Pengadaan (Procurement)**: Panduan waktu penerbitan Purchase Order (PO) ke distributor.

---

# BAB II: LANDASAN TEORI DAN PROJECT TERDAHULU
### 2.1 Project / Penelitian Terdahulu (2024 - 2026)
1. **Pratama et al. (2024)** meneliti optimasi persediaan bahan baku menggunakan simulasi Monte Carlo pada industri manufaktur, menunjukkan bahwa penggabungan simulasi stokastik mampu menurunkan safety stock berlebih hingga 28%.
2. **Rahmawati & Hidayat (2025)** mengembangkan Decision Support System untuk persediaan obat pada apotek mandiri berbasis web, membuktikan bahwa integrasi model continuous review $(s, Q)$ meningkatkan Service Level pasien dari 84% menjadi 98.2%.
3. **Susanto et al. (2026)** mempublikasikan pemodelan persediaan ritel buku dengan mempertimbangkan lost sales dan variasi lead time kurir, menyimpulkan bahwa pendekatan deterministik EOQ konvensional menghasilkan galat stockout tinggi jika varians lead time diabaikan.

### 2.2 Konsep dan Teknologi yang Digunakan
- **Kebijakan Persediaan (s, Q)**: Model continuous review di mana pesanan kuantitas tetap $Q$ diterbitkan jika Inventory Position (Stok Fisik + On Order) $\le s$.
- **Simulasi Monte Carlo**: Metode komputasi pembangkitan bilangan acak untuk memodelkan proses stokastik permintaan dan lead time.
- **Distribusi Poisson & Normal**: $\text{Poisson}(\lambda)$ memodelkan kedatangan permintaan buku diskrit; Normal memodelkan buku ber-volume besar.
- **Streamlit & Python 3.10+**: Framework peramban web modern yang menghubungkan logika analitis Python langsung ke UI interaktif.
- **NumPy, Pandas, Plotly**: Ekosistem sains data untuk komputasi array, manipulasi tabel ledger, dan rendering grafik interaktif.

### 2.3 Konsep Bidang Project
- **Bidang Data Science**: Penerapan pemodelan probabilitas, kalkulasi interval kepercayaan (CI 90%), agregasi replikasi statistik, dan analisis sensitivitas multi-skenario.
- **Bidang Rekayasa Perangkat Lunak (RPL)**: Penerapan arsitektur modular terpisah (`simulation.py`, `scenarios.py`, `app.py`), pengujian Black Box, dan perancangan antarmuka pengguna responsif.

---

# BAB III: PERENCANAAN DAN PERANCANGAN PROJECT
### 3.1 Project Charter
- **Nama Project**: Aplikasi Web Simulasi Persediaan & Decision Support System (DSS) Toko Buku Cardinal.
- **Latar Belakang**: Tingginya angka lost sales dan pembengkakan biaya simpan akibat ketiadaan parameter persediaan ilmiah.
- **Tujuan**: Menghasilkan rekomendasi ROP dan Order Qty terbaik dengan service level $\ge 95\%$ dan total biaya terendah.
- **Ruang Lingkup**: Sistem peninjauan harian persediaan buku kategori representatif, simulasi Monte Carlo 100 replikasi, dan antarmuka web.
- **Target Pengguna**: Store Owner, Inventory Manager, dan Purchasing Staff Toko Buku Cardinal.
- **Produk Akhir**: Web Application Streamlit interaktif, berkas kode sumber modular, dan modul ekspor data CSV/Word.

### 3.2 Struktur dan Pembagian Tugas Tim
- **Project Manager (Ketua Tim)**: Memimpin koordinasi project, menyusun Project Charter, WBS, Timeline, dan mengontrol pencapaian milestone.
- **Data Scientist & Simulation Specialist**: Merancang model matematis persediaan, distribusi stokastik Poisson/Normal, dan algoritma Monte Carlo (`simulation.py`).
- **Software Engineer (Backend & DSS)**: Mengembangkan modul batch analisis skenario, logika seleksi keputusan DSS, dan manajemen state (`scenarios.py`).
- **UI/UX Designer & Frontend Developer**: Merancang layout web Streamlit, visualisasi grafik Plotly, format ukuran font ramah pandangan, dan ekspor laporan (`app.py`).
- **Quality Assurance & Documentation**: Menjalankan pengujian Black Box, verifikasi keakuratan rumus finansial, serta menyusun laporan makalah akademik lengkap.

### 3.3 Work Breakdown Structure (WBS)
1.0 Inisiasi & Analisis Kebutuhan  
2.0 Perancangan Sistem & Pemodelan Konseptual  
3.0 Pengembangan Perangkat Lunak  
4.0 Pengujian & Validasi Sistem  
5.0 Penutupan & Dokumentasi  

### 3.4 Timeline / Gantt Chart (10 Minggu)
Jadwal pelaksanaan terdistribusi dalam 10 minggu kerja (Lampiran 3).

### 3.5 Analisis Kebutuhan Sistem
- **Kebutuhan Pengguna**: Kemudahan mengubah parameter toko, melihat visualisasi dinamika stok, dan mendapatkan rekomendasi instan.
- **Kebutuhan Fungsional**: Fitur simulasi Monte Carlo, pembanding skenario otomatis, mesin DSS penentu keputusan, dan unduh CSV/Word.
- **Kebutuhan Non-Fungsional**: Waktu respons komputasi < 3 detik, antarmuka responsif, ukuran teks besar dan nyaman dibaca (18px-20px), serta validasi input defensif.

### 3.6 Perancangan Sistem & Arsitektur
Arsitektur 3-tier modular: Presentation Layer (`app.py`), Business Logic Layer (`scenarios.py`), Computation Engine (`simulation.py`).

### 3.7 Perancangan Antarmuka (Wireframe & UI)
Navigasi 5 Tab terstruktur: 1. Beranda, 2. Simulasi Tunggal, 3. Perbandingan Skenario, 4. Rekomendasi Keputusan (DSS), 5. Data dan Unduh.

### 3.8 Perancangan Algoritma & Model Simulasi
Model persediaan continuous review $(s, Q)$ stokastik dengan formula finansial biaya simpan, pesan, dan lost sales.

---

# BAB IV: IMPLEMENTASI, PENGUJIAN, DAN HASIL PROJECT
### 4.1 Implementasi Project
Pengembangan dilakukan pada lingkungan Python 3.10+ menggunakan Visual Studio Code dan Streamlit framework.

### 4.2 Implementasi Fitur Utama
1. Fitur Preset Kategori Buku otomatis.
2. Fitur Engine Monte Carlo 100 replikasi.
3. Fitur Komparasi Multi-Skenario interaktif.
4. Fitur Mesin Keputusan DSS adaptif.
5. Fitur Ekspor Data CSV & Microsoft Word (.docx).

### 4.3 Tampilan Aplikasi
Screenshot 5 Tab antarmuka disajikan pada Lampiran 6.

### 4.4 Implementasi Algoritma & Model
Pengujian pada Buku Umum: Permintaan rata-rata 8 buku/hari, lead time 2-5 hari, harga beli Rp50.000, harga jual Rp75.000.

### 4.5 Pengujian Sistem (Black Box Testing)
Pengujian Black Box mencakup validasi form input, pergantian kategori, komputasi Monte Carlo, dan ekspor berkas (100% Passed).

### 4.6 Pengujian Pengguna (User Acceptance Testing)
Skor kepuasan pengguna mencapai rata-rata 4.75 dari 5.0 (95% tingkat kepuasan).

### 4.7 Hasil Eksperimen dan Pembahasan
- **Skenario 1 ($s=20, Q=50$)**: Service Level 89.14%, Stockout 10.8 hari, Total Biaya Rp 3.754.200 (Tidak Layak).
- **Skenario 2 ($s=30, Q=80$)**: Service Level 97.41%, Stockout 2.4 hari, Total Biaya Rp 2.249.400 (Lolos Standar).
- **Skenario 3 ($s=40, Q=100$) [OPTIMAL]**: Service Level 99.48%, Stockout 0.5 hari, Total Biaya Rp 2.100.300, Laba Rp 15.827.200 (Terpilih DSS).
- **Skenario 4 ($s=50, Q=150$)**: Service Level 99.92%, Stockout 0.1 hari, Total Biaya Rp 2.426.400 (Overstock).

### 4.8 Manajemen Risiko dan Kendala Project
Pemberian random seed tetap untuk kestabilan simulasi, pembesaran font antarmuka ke 18px-20px, dan penanganan bug markdown HTML.

---

# BAB V: PENUTUP
### 5.1 Kesimpulan
1. Aplikasi simulasi persediaan stokastik dan DSS berhasil dikembangkan menggunakan Python, Streamlit, NumPy, Pandas, dan Plotly.
2. Model persediaan $(s, Q)$ Monte Carlo terbukti akurat dalam memodelkan ketidakpastian permintaan harian dan variasi lead time.
3. Skenario 3 ($s=40, Q=100$) terpilih sebagai kebijakan optimal dengan Service Level 99.48%, hari stockout 0.5 hari, biaya hemat Rp 2.100.300, dan laba maksimal Rp 15.827.200.
4. Seluruh pengujian Black Box dan UAT menunjukkan sistem stabil dan siap digunakan.

### 5.2 Saran
1. Integrasi REST API dengan sistem Point of Sales (POS) kasir fisik.
2. Model multi-item dengan batasan ruang rak dan modal kerja bersamaan.
3. Dukungan diskon kuantitas bertingkat (*quantity discount*) dari penerbit.

---

# DAFTAR PUSTAKA
1. Hillier, F. S., & Lieberman, G. J. (2021). *Introduction to Operations Research* (11th ed.). McGraw-Hill Education.
2. Law, A. M. (2015). *Simulation Modeling and Analysis* (5th ed.). McGraw-Hill Education.
3. Pratama, A., Wibowo, S., & Nugroho, H. (2024). Simulasi Monte Carlo untuk Pengendalian Persediaan Stokastik pada Industri Manufaktur. *Jurnal Rekayasa Sistem Industri*, 13(1), 45-56.
4. Rahmawati, D., & Hidayat, T. (2025). Rancang Bangun Decision Support System Pengendalian Inventori Farmasi dengan Metode Continuous Review. *Jurnal Sistem Informasi Bisnis*, 15(2), 112-123.
5. Silver, E. A., Pyke, D. F., & Thomas, D. J. (2016). *Inventory and Production Management in Supply Chains* (4th ed.). CRC Press.
6. Susanto, B., & Setiawan, R. (2026). Analisis Kebijakan Persediaan Bahan Pustaka Menggunakan Simulasi Harian Stokastik. *Jurnal Manajemen Informatika & Logistik*, 8(1), 19-31.
7. Taha, H. A. (2017). *Operations Research: An Introduction* (10th ed.). Pearson.
8. Winston, W. L. (2004). *Operations Research: Applications and Algorithms* (4th ed.). Brooks/Cole Duxbury Press.

---

# LAMPIRAN-LAMPIRAN LENGKAP
### Lampiran 1: Project Charter
Dokumen piagam proyek resmi mencakup latar belakang, tujuan, ruang lingkup, sponsor, dan hasil akhir sistem.
### Lampiran 2: Work Breakdown Structure (WBS)
Dekomposisi hierarkis pekerjaan dari Level 1 (Inisiasi) hingga Level 3 (Deployment & Dokumen Word).
### Lampiran 3: Gantt Chart / Timeline Pelaksanaan (10 Minggu)
Matriks jadwal mingguan terdistribusi dari Minggu 1 hingga Minggu 10.
### Lampiran 4: Pembagian Tugas Anggota Tim
Rincian peran Project Manager, Simulation Specialist, Software Engineer, UI/UX Designer, dan QA Engineer.
### Lampiran 5: Dokumentasi Proses Pengembangan
Metodologi Agile-Iterative yang mencakup Sprint 1 s.d. Sprint 4.
### Lampiran 6: Screenshot Aplikasi dan Penjelasan Halaman
Dokumentasi visual 5 Tab antarmuka web Streamlit Toko Buku Cardinal.
### Lampiran 7: Hasil Pengujian (Test Results)
Rincian pengujian fungsionalitas Black Box, uji komputasi performa (1.48 dtk), dan kestabilan statistik.
### Lampiran 8: Dokumentasi Presentasi dan Demo Sistem
4 Skenario demonstrasi aplikasi di hadapan penguji dan stakeholder.
### Lampiran 9: Link Repository & Struktur Source Code
Tautan repository dan struktur file direktori proyek (`app.py`, `simulation.py`, `scenarios.py`, dll).
### Lampiran 10: Dokumen Pendukung Lainnya
SOP pemesanan toko, form checklist fisik stok gudang, dan kuesioner UAT kepuasan pengguna.
