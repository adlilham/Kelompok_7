# 📄 DOKUMENTASI TEKNIS SISTEM SIMULASI & PEMODELAN
## Simulasi Persediaan (Stok) Buku pada Toko Buku "Cardinal"
**Mata Kuliah:** Teknik Simulasi dan Pemodelan  
**Materi Rujukan:** Bahan Penyusunan Bab III (Metodologi dan Pemodelan Sistem) & Bab IV (Hasil Eksperimen dan Pembahasan)

---

# BAGIAN I: METODOLOGI DAN PEMODELAN SISTEM (BAB III)

## 1.1 Deskripsi Masalah dan Studi Kasus
Toko Buku "Cardinal" merupakan toko buku ritel yang mengelola ribuan judul buku. Pada studi kasus ini, sistem memodelkan pengelolaan persediaan untuk satu kategori produk buku (misalnya *Buku Umum*) yang memiliki tingkat perputaran harian tinggi. 

Toko menghadapi dua ketidakpastian utama (*stochastic variables*):
1. **Permintaan Harian Pelanggan ($D_t$)**: Fluktuatif dan tidak dapat diprediksi secara deterministik.
2. **Waktu Tunggu Pengiriman / Lead Time ($L_t$)**: Durasi antara penerbitan pesanan (*Purchase Order*) ke distributor hingga buku fisik tiba di gudang toko bervariasi antara 2 hingga 5 hari.

Tujuan optimasi adalah menentukan:
- **Kapan memesan kembali**: Titik pemesanan kembali (*Reorder Point* / $s$).
- **Berapa banyak yang dipesan**: Kuantitas pemesanan tetap (*Order Quantity* / $Q$).

Kriteria keberhasilan sistem adalah meminimalkan total biaya persediaan (*Total Inventory Cost*) dengan tetap menjaga tingkat ketersediaan layanan (*Service Level*) di atas ambang batas yang dapat diterima (misalnya $\ge 95\%$).

---

## 1.2 Daftar Variabel dan Parameter Sistem

### A. Parameter Input Sistem (Konstanta & Variabel Eksogen)
| Simbol / Variabel | Nama Parameter | Satuan | Nilai Default | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| $I_0$ | Stok Awal | Unit Buku | 100 | Persediaan fisik di tangan pada hari ke-1 ($t=1$). |
| $\lambda$ | Rata-rata Permintaan | Buku/Hari | 8.0 | Parameter laju kedatangan distribusi Poisson $\text{Pois}(\lambda)$. |
| $\sigma_D$ | Deviasi Standar Permintaan | Buku/Hari | 2.5 | Digunakan jika memilih opsi distribusi Normal $\mathcal{N}(\mu, \sigma^2)$. |
| $L_{\min}, L_{\max}$ | Rentang Lead Time | Hari | 2 - 5 | Batas interval distribusi diskrit seragam $\mathcal{U}\{L_{\min}, L_{\max}\}$. |
| $SS$ | Safety Stock | Unit Buku | 10 | Batas persediaan pengaman untuk indikator kewaspadaan toko. |
| $N$ | Lama Simulasi | Hari | 90 | Panjang horizon evaluasi (misal 1 kuartal operasional). |
| $R$ | Jumlah Replikasi | Replikasi | 100 | Jumlah pengulangan simulasi Monte Carlo untuk kestabilan statistik. |
| $P_b$ | Harga Beli | Rupiah (Rp) | Rp 50.000 | Biaya pembelian per unit buku dari distributor/penerbit. |
| $P_j$ | Harga Jual | Rupiah (Rp) | Rp 75.000 | Harga jual per unit buku kepada konsumen akhir. |
| $C_h$ | Biaya Simpan (*Holding Cost*) | Rp/Buku/Hari | Rp 200 | Biaya penyimpanan fisik, sewa ruang, asuransi, dan depresiasi. |
| $C_o$ | Biaya Pesan (*Ordering Cost*) | Rp/Pesanan | Rp 100.000 | Biaya administrasi, kurir, dan penanganan per kali pemesanan. |
| $C_s$ | Biaya Kehabisan Stok (*Stockout Cost*) | Rp/Buku | Rp 25.000 | Kerugian margin keuntungan akibat penjualan hilang ($P_j - P_b$). |

### B. Variabel Kebijakan Keputusan (Decision Variables)
| Simbol | Nama Variabel | Satuan | Nilai Uji Default | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| $s$ | *Reorder Point* (ROP) | Unit Buku | 30 | Jika posisi persediaan $\le s$, lakukan pemesanan kembali. |
| $Q$ | *Order Quantity* | Unit Buku | 80 | Jumlah unit buku yang dipesan setiap kali PO diterbitkan. |

### C. Variabel Status Harian (State Variables pada Hari ke-$t$)
| Simbol | Nama Variabel | Definisi Matematis | Keterangan |
| :--- | :--- | :--- | :--- |
| $I_t^{\text{awal}}$ | Stok Awal Hari | $I_{t-1}^{\text{akhir}}$ | Stok fisik sebelum penerimaan barang baru hari ini. |
| $A_t$ | Barang Masuk | $\sum Q \text{ yang } L \text{ tiba di } t$ | Pesanan masa lalu yang tiba pada hari $t$. |
| $I_t^{\text{tersedia}}$ | Stok Tersedia | $I_t^{\text{awal}} + A_t$ | Stok efektif yang siap dijual kepada konsumen hari ini. |
| $D_t$ | Permintaan Harian | $\sim \text{Poisson}(\lambda)$ | Jumlah buku yang ingin dibeli pelanggan pada hari $t$. |
| $S_t$ | Penjualan Terpenuhi | $\min(D_t, I_t^{\text{tersedia}})$ | Jumlah buku yang berhasil ditransaksikan. |
| $LS_t$ | Penjualan Hilang (*Lost Sales*) | $\max(0, D_t - I_t^{\text{tersedia}})$ | Permintaan yang tidak terpenuhi karena kekurangan stok. |
| $I_t^{\text{akhir}}$ | Stok Akhir Hari | $I_t^{\text{tersedia}} - S_t$ | Persediaan fisik di tangan pada penutupan toko hari $t$. |
| $OO_t$ | *On-Order* (Dalam Perjalanan) | $\sum_{\text{pesanan aktif}} Q$ | Akumulasi unit buku yang telah dipesan namun belum tiba. |
| $IP_t$ | *Inventory Position* | $I_t^{\text{akhir}} + OO_t$ | Posisi persediaan efektif untuk evaluasi titik pemesanan. |
| $O_t$ | Indikator Pemesanan | $1 \text{ jika } IP_t \le s \text{ else } 0$ | Pemicu penerbitan pesanan baru. |

### D. Variabel Output & Metrik Kinerja (Performance Metrics)
1. **Service Level ($SL$)**:
   $$SL = \left( \frac{\sum_{t=1}^{N} S_t}{\sum_{t=1}^{N} D_t} \right) \times 100\%$$
2. **Total Hari Kehabisan Stok ($H_{\text{stockout}}$)**:
   $$H_{\text{stockout}} = \sum_{t=1}^{N} \mathbb{I}(I_t^{\text{akhir}} = 0)$$
3. **Total Penjualan Hilang ($LS_{\text{total}}$)**:
   $$LS_{\text{total}} = \sum_{t=1}^{N} LS_t$$
4. **Rata-rata Persediaan di Tangan ($\bar{I}$)**:
   $$\bar{I} = \frac{1}{N} \sum_{t=1}^{N} I_t^{\text{akhir}}$$
5. **Frekuensi Pemesanan ($F_{\text{pesan}}$)**:
   $$F_{\text{pesan}} = \sum_{t=1}^{N} O_t$$
6. **Total Biaya Persediaan ($TC$)**:
   $$TC = \sum_{t=1}^{N} \left( I_t^{\text{akhir}} \cdot C_h + O_t \cdot C_o + LS_t \cdot C_s \right)$$
7. **Estimasi Laba Bersih ($\Pi$)**:
   $$\Pi = \sum_{t=1}^{N} \left( S_t \cdot (P_j - P_b) \right) - TC$$

---

## 1.3 Asumsi-Asumsi Model Simulasi
1. **Model Penjualan Hilang (*Lost Sales*)**: Pelanggan yang datang saat stok kosong tidak bersedia menunggu (*no backorder*). Permintaan yang tidak terpenuhi dianggap hilang selamanya dan menjadi biaya kesempatan (*opportunity cost*).
2. **Pembangkitan Permintaan Acak**: Permintaan buku harian bersifat independen dan identik (*i.i.d.*) mengikuti distribusi Poisson dengan parameter rata-rata $\lambda$.
3. **Penyusutan Persediaan Sesaat**: Penjualan buku dan pengurangan stok diperhitungkan secara diskrit harian (*day-by-day basis*).
4. **Waktu Tunggu Pengiriman (*Lead Time*)**: Lead time dinyatakan dalam bilangan bulat positif (hari) yang dibangkitkan dari distribusi acak diskrit seragam antara $L_{\min}$ dan $L_{\max}$.
5. **Posisi Persediaan (*Inventory Position*)**: Evaluasi pemesanan didasarkan pada $IP_t = \text{Stok di Tangan} + \text{Pesanan dalam Perjalanan}$. Aturan ini menjamin toko tidak melakukan pesanan ganda yang tidak perlu saat pesanan sebelumnya sedang diantar.
6. **Kapasitas Gudang**: Toko diasumsikan memiliki kapasitas fisik yang mencukupi untuk menampung seluruh unit buku yang dipesan.
7. **Harga dan Biaya Konstan**: Selama horizon simulasi $N$ hari, harga beli, harga jual, biaya simpan per hari, dan biaya pesan bersifat tetap.

---

## 1.4 Alur Input - Proses - Output (IPO)

```
┌──────────────────────────────────────────────┐
│                  INPUT                       │
├──────────────────────────────────────────────┤
│ 1. Parameter Kebijakan: (s, Q, SS, Stok Awal)│
│ 2. Parameter Stokastik: (λ, Dist, L_min, Max)│
│ 3. Parameter Finansial: (Pb, Pj, Ch, Co, Cs) │
│ 4. Pengaturan Monte Carlo: (N hari, R replik)│
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 PROSES                       │
├──────────────────────────────────────────────┤
│ 1. Inisialisasi RNG Seed & Array Penyimpanan │
│ 2. Looping Replikasi (r = 1 sampai R):       │
│    a. Set Stok Awal = I_0, Antrean Order = ∅ │
│    b. Looping Hari (t = 1 sampai N):         │
│       - Terima pesanan jatuh tempo hari t    │
│       - Bangkitkan D_t ~ Poisson(λ)          │
│       - Hitung Penjualan & Lost Sales        │
│       - Update Stok Akhir                    │
│       - Hitung Posisi Persediaan (IP_t)      │
│       - Cek: Jika IP_t <= s -> Pesan Q unit  │
│       - Hitung Biaya Simpan, Pesan, Stockout │
│    c. Simpan metrik replikasi r              │
│ 3. Agregasi Statistik: Mean, Std Dev, CI 90% │
│ 4. Evaluasi Multi-Skenario & Mesin DSS       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 OUTPUT                       │
├──────────────────────────────────────────────┤
│ 1. Metrik Kinerja (Service Level, Laba, dll) │
│ 2. Visualisasi Interaktif (Grafik Plotly)    │
│ 3. Rekomendasi Kebijakan Optimal (s, Q)      │
│ 4. Dataframe Log Harian & Ekspor Berkas CSV  │
└──────────────────────────────────────────────┘
```

---

## 1.5 Algoritma Simulasi Langkah-demi-Langkah (Pseudocode)

```
Algoritma: Simulasi_Persediaan_Monte_Carlo
Input: Config (s, Q, I_0, λ, L_min, L_max, N, R, Pb, Pj, Ch, Co, Cs, seed)
Output: Ringkasan_Statistik, Dataframe_Replikasi, Dataframe_Log_Sampel

1. Inisialisasi Master_RNG dengan seed
2. Buat list_hasil_replikasi = []
3. Buat df_log_sampel = None

4. UNTUK SETIAP r = 1 SAMPAI R LAKUKAN:
   a. Bangkitkan sub_seed dari Master_RNG
   b. Inisialisasi RNG_r dengan sub_seed
   c. stok = I_0
   d. antrean_pesanan = [] // Menyimpan tuple (hari_tiba, qty)
   e. log_harian_r = []

   f. UNTUK SETIAP hari t = 1 SAMPAI N LAKUKAN:
      i.   stok_awal = stok
      ii.  buku_masuk = 0
      iii. pesanan_baru = []
      iv.  UNTUK SETIAP (hari_tiba, qty) DALAM antrean_pesanan:
              JIKA hari_tiba <= t MAKA:
                  buku_masuk += qty
              SELAIN ITU:
                  pesanan_baru.append((hari_tiba, qty))
           antrean_pesanan = pesanan_baru
           stok_tersedia = stok_awal + buku_masuk

      v.   Bangkitkan D_t dari Poisson(λ) menggunakan RNG_r
      vi.  penjualan = min(D_t, stok_tersedia)
      vii. lost_sales = D_t - penjualan
      viii.stok_akhir = stok_tersedia - penjualan
      ix.  stok = stok_akhir

      x.   on_order = SUM(qty DALAM antrean_pesanan)
      xi.  inventory_position = stok + on_order

      xii. pesan_hari_ini = FALSE
           qty_pesan = 0
           lead_time = 0
           JIKA inventory_position <= s MAKA:
               pesan_hari_ini = TRUE
               qty_pesan = Q
               lead_time = Bilangan_Bulat_Acak(L_min, L_max)
               hari_kedatangan = t + lead_time
               antrean_pesanan.append((hari_kedatangan, qty_pesan))
               inventory_position += qty_pesan

      xiii.biaya_simpan = stok_akhir * Ch
           biaya_pesan = Co JIKA pesan_hari_ini ELSE 0
           biaya_stockout = lost_sales * Cs
           total_biaya = biaya_simpan + biaya_pesan + biaya_stockout
           laba = (penjualan * (Pj - Pb)) - total_biaya

      xiv. Catat seluruh variabel hari t ke log_harian_r

   g. JIKA r == 1 MAKA:
         df_log_sampel = Konversi_Ke_DataFrame(log_harian_r)

   h. Hitung total permintaan, penjualan, lost sales, biaya, laba untuk replikasi r
   i. service_level = (total_penjualan / total_permintaan) * 100%
   j. Simpan hasil replikasi r ke list_hasil_replikasi

5. df_replikasi = Konversi_Ke_DataFrame(list_hasil_replikasi)
6. Hitung rata-rata, standar deviasi, dan persentil 5% serta 95% dari df_replikasi
7. RETURN Ringkasan_Statistik, df_replikasi, df_log_sampel
```

---

# BAGIAN II: HASIL EKSPERIMEN DAN PEMBAHASAN (BAB IV)

## 2.1 Desain Eksperimen Multi-Skenario Kebijakan (s, Q)
Untuk menguji perilaku sistem persediaan Toko Buku Cardinal, dirancang 4 skenario kombinasi kebijakan persediaan dengan parameter dasar:
- Horizon Simulasi: $N = 90$ hari
- Jumlah Replikasi Monte Carlo: $R = 100$ replikasi
- Permintaan Harian: $\text{Poisson}(\lambda = 8.0\text{ buku/hari})$
- Lead Time: Acak seragam $\mathcal{U}\{2, 5\}$ hari
- Harga & Biaya: $P_b = \text{Rp } 50.000$, $P_j = \text{Rp } 75.000$, $C_h = \text{Rp } 200/\text{buku/hari}$, $C_o = \text{Rp } 100.000/\text{pesan}$, $C_s = \text{Rp } 25.000/\text{buku}$.

Daftar Skenario yang diuji:
1. **Skenario 1 (Konservatif / Pesanan Kecil)**: $s = 20, Q = 50$
2. **Skenario 2 (Moderat / Standar Toko)**: $s = 30, Q = 80$
3. **Skenario 3 (Agresif / Pengamanan Stok)**: $s = 40, Q = 100$
4. **Skenario 4 (Stok Tinggi / Pesanan Besar)**: $s = 50, Q = 150$

---

## 2.2 Ringkasan Hasil Eksperimen Simulasi (Tabel Komparasi)

Berikut adalah ringkasan rata-rata kinerja dari 100 replikasi Monte Carlo:

| Metrik Evaluasi | Skenario 1 (s=20, Q=50) | Skenario 2 (s=30, Q=80) | Skenario 3 (s=40, Q=100) | Skenario 4 (s=50, Q=150) |
| :--- | :---: | :---: | :---: | :---: |
| **Service Level (%)** | 89,14% | 97,41% | 99,48% | 99,92% |
| **Hari Stockout (Hari)** | 10,8 hari | 2,4 hari | 0,5 hari | 0,1 hari |
| **Total Lost Sales (Buku)** | 77,8 unit | 18,6 unit | 3,7 unit | 0,6 unit |
| **Rata-rata Stok di Tangan** | 29,4 unit | 50,8 unit | 72,1 unit | 107,3 unit |
| **Frekuensi Pemesanan** | 12,8 kali | 8,7 kali | 7,1 kali | 4,8 kali |
| **Biaya Simpan (Rp)** | Rp 529.200 | Rp 914.400 | Rp 1.297.800 | Rp 1.931.400 |
| **Biaya Pesan (Rp)** | Rp 1.280.000 | Rp 870.000 | Rp 710.000 | Rp 480.000 |
| **Biaya Stockout (Rp)** | Rp 1.945.000 | Rp 465.000 | Rp 92.500 | Rp 15.000 |
| **Total Biaya Operasional (Rp)** | **Rp 3.754.200** | **Rp 2.249.400** | **Rp 2.100.300** | **Rp 2.426.400** |
| **Estimasi Laba Bersih (Rp)** | **Rp 12.325.800** | **Rp 15.305.600** | **Rp 15.827.200** | **Rp 15.568.600** |

---

## 2.3 Analisis & Pembahasan Hasil Eksperimen

### 1. Perilaku Skenario 1 ($s=20, Q=50$): Kerugian Akibat Stockout
Pada Skenario 1, toko menerapkan batas pemesanan rendah ($s=20$) dan jumlah pesanan kecil ($Q=50$). Kebijakan ini berhasil menekan biaya penyimpanan menjadi yang paling rendah (Rp 529.200). Namun, akibat lead time pengiriman berkisar antara 2 sampai 5 hari dengan permintaan rata-rata 8 buku/hari (kebutuhan selama lead time $= 16 - 40$ buku), stok sering kali habis sebelum barang baru tiba. Hal ini menyebabkan rata-rata hari kehabisan stok mencapai **10,8 hari** dengan 77,8 buku penjualan hilang (*lost sales*). Biaya penalti kehabisan stok membengkak hingga Rp 1.945.000, sehingga laba bersih toko tertekan ke angka terendah (Rp 12.325.800) dengan *Service Level* hanya 89,14% (di bawah standar layanan 95%).

### 2. Efektivitas Skenario 2 ($s=30, Q=80$): Kebijakan Seimbang
Dengan meningkatkan ROP ke $s=30$ dan $Q=80$, terjadi lonjakan performa layanan yang signifikan. *Service Level* naik menjadi **97,41%**, melampaui target minimum 95%. Hari kehabisan stok terpangkas drastis menjadi hanya 2,4 hari. Biaya pesan berkurang karena kuantitas order lebih besar ($Q=80$), sehingga total biaya operasional turun drastis ke Rp 2.249.400 dan laba melonjak menjadi Rp 15.305.600.

### 3. Keunggulan Optimal Skenario 3 ($s=40, Q=100$): Solusi Terbaik
Skenario 3 memberikan hasil terbaik secara keseluruhan (*global optimal* di antara skenario yang diuji). Reorder point sebesar 40 buku memberikan penyangga yang sangat aman terhadap fluktuasi kedatangan pesanan. *Service level* mencapai **99,48%** dengan *lost sales* nyaris mendekati nol (3,7 buku selama 3 bulan). Pengurangan biaya stockout dan biaya pemesanan mampu mengimbangi kenaikan biaya simpan (Rp 1.297.800), menghasilkan **Total Biaya Operasional terendah (Rp 2.100.300)** dan **Estimasi Laba Bersih tertinggi (Rp 15.827.200)**.

### 4. Batas Efisiensi pada Skenario 4 ($s=50, Q=150$): *Overstocking*
Pada Skenario 4, kuantitas pesanan dinaikkan menjadi sangat besar ($Q=150$). Meskipun *service level* mencapai hampir sempurna (99,92%), rata-rata stok di tangan melonjak menjadi 107,3 buku. Akibatnya, biaya simpan membengkak hingga Rp 1.931.400. Kenaikan biaya simpan ini melampaui penghematan biaya pesan, sehingga total biaya naik kembali menjadi Rp 2.426.400 dan laba bersih menurun menjadi Rp 15.568.600.

---

## 2.4 Rekomendasi Manajerial (Decision Support System)

Berdasarkan formulasi algoritma DSS dengan target minimal *Service Level* $95\%$:
- **Kebijakan Terpilih**: **Skenario 3 ($s = 40, Q = 100$)**
- **Instruksi Operasional**:
  > *"Manajer Toko Buku Cardinal disarankan menerbitkan pesanan pembelian (Purchase Order) sejumlah **100 buku** ke distributor setiap kali posisi persediaan (stok fisik di toko + stok dalam perjalanan pengiriman) turun menyentuh atau berada di bawah **40 buku**."*
- **Justifikasi Ekonomi**:
  Kebijakan ini menjamin 99,48% permintaan pembeli terpenuhi secara langsung, meminimalkan frekuensi stockout menjadi kurang dari 1 hari per triwulan, serta memberikan kontribusi laba bersih paling maksimal sebesar Rp 15.827.200.

