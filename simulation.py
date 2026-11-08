"""
simulation.py - Modul Inti Simulasi Persediaan Toko Buku Cardinal
Mata Kuliah: Teknik Simulasi dan Pemodelan

Modul ini mengimplementasikan simulasi Monte Carlo harian untuk kebijakan
pengendalian persediaan kontinu (s, Q) pada Toko Buku Cardinal.
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd


@dataclass
class SimulationConfig:
    """Konfigurasi parameter simulasi persediaan (s, Q)."""
    # Parameter Kebijakan
    reorder_point: int = 30
    order_quantity: int = 80
    safety_stock: int = 10
    stok_awal: int = 100

    # Parameter Permintaan & Lead Time
    distribusi_permintaan: str = "Poisson"  # "Poisson" atau "Normal"
    rata_permintaan: float = 8.0
    std_permintaan: float = 2.5
    lead_time_min: int = 2
    lead_time_max: int = 5
    lead_time_mode: str = "Acak"  # "Acak" atau "Tetap"

    # Parameter Simulasi Monte Carlo
    periode_hari: int = 90
    jumlah_replikasi: int = 100
    random_seed: Optional[int] = 42

    # Parameter Finansial (Rupiah)
    harga_beli: float = 50000.0
    harga_jual: float = 75000.0
    biaya_simpan_per_hari: float = 200.0
    biaya_pesan_per_order: float = 100000.0
    biaya_stockout_per_unit: Optional[float] = None  # None = otomatis margin laba


def generate_permintaan(
    tipe_distribusi: str,
    rata_rata: float,
    std_dev: float,
    ukuran: int,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Membangkitkan data permintaan harian acak.
    Mendukung distribusi Poisson (diskrit) dan Normal (kontinu dibulatkan & dibatasi non-negatif).
    """
    if tipe_distribusi == "Poisson":
        permintaan = rng.poisson(lam=max(0.1, rata_rata), size=ukuran)
    else:  # Normal
        permintaan = np.round(rng.normal(loc=rata_rata, scale=max(0.01, std_dev), size=ukuran))
        permintaan = np.maximum(0, permintaan).astype(int)
    return permintaan


def simulasi_satu_replikasi(
    config: SimulationConfig,
    rng: np.random.Generator
) -> pd.DataFrame:
    """
    Menjalankan simulasi persediaan harian untuk 1 siklus horizon (N hari).
    
    Logika Harian:
    1. Awal hari: Stok bertambah jika ada pesanan dalam perjalanan yang tiba hari ini.
    2. Permintaan harian dibangkitkan.
    3. Pemenuhan permintaan:
       - Penjualan = min(Permintaan, Stok Tersedia)
       - Lost Sales = Permintaan - Penjualan (jika Permintaan > Stok)
       - Stok berkurang sebesar Penjualan.
    4. Evaluasi Posisi Persediaan (Inventory Position):
       - Posisi Persediaan = Stok di Tangan + Pesanan dalam Perjalanan (on-order)
       - Jika Posisi Persediaan <= Reorder Point (s):
         Buat pesanan baru sebesar Order Quantity (Q).
         Tentukan lead time dan jadwalkan hari kedatangan pesanan.
    5. Hitung biaya harian (simpan, pesan, lost sales) dan estimasi pendapatan/laba.
    """
    margin_laba = max(0.0, config.harga_jual - config.harga_beli)
    biaya_stockout_unit = (
        config.biaya_stockout_per_unit
        if config.biaya_stockout_per_unit is not None
        else margin_laba
    )

    permintaan_harian = generate_permintaan(
        tipe_distribusi=config.distribusi_permintaan,
        rata_rata=config.rata_permintaan,
        std_dev=config.std_permintaan,
        ukuran=config.periode_hari,
        rng=rng
    )

    stok_di_tangan = int(config.stok_awal)
    # List menyimpan tuple (hari_tiba, qty_pesanan)
    pesanan_dalam_perjalanan = []
    
    log_harian = []

    for hari in range(1, config.periode_hari + 1):
        stok_awal_hari = stok_di_tangan

        # 1. Penerimaan pesanan yang jatuh tempo hari ini
        pesanan_tiba = 0
        pesanan_tersisa = []
        for hari_tiba, qty in pesanan_dalam_perjalanan:
            if hari_tiba <= hari:
                pesanan_tiba += qty
            else:
                pesanan_tersisa.append((hari_tiba, qty))
        pesanan_dalam_perjalanan = pesanan_tersisa
        stok_setelah_terima = stok_awal_hari + pesanan_tiba

        # 2. Permintaan hari ini
        demand = int(permintaan_harian[hari - 1])

        # 3. Penjualan & Lost Sales
        terjual = min(demand, stok_setelah_terima)
        lost_sales = demand - terjual
        stok_akhir = stok_setelah_terima - terjual
        stok_di_tangan = stok_akhir

        # 4. Posisi Persediaan & Pengecekan Reorder Point
        # Total unit on-order (sedang dalam perjalanan)
        total_on_order = sum(qty for _, qty in pesanan_dalam_perjalanan)
        posisi_persediaan = stok_di_tangan + total_on_order

        pesan_hari_ini = False
        qty_dipesan = 0
        lead_time_hari = 0

        if posisi_persediaan <= config.reorder_point:
            pesan_hari_ini = True
            qty_dipesan = int(config.order_quantity)
            
            # Penentuan lead time
            if config.lead_time_mode == "Tetap" or config.lead_time_min >= config.lead_time_max:
                lead_time_hari = int(config.lead_time_min)
            else:
                lead_time_hari = int(rng.integers(config.lead_time_min, config.lead_time_max + 1))
            
            hari_tiba = hari + lead_time_hari
            pesanan_dalam_perjalanan.append((hari_tiba, qty_dipesan))
            # Posisi persediaan terupdate dengan pesanan baru
            posisi_persediaan += qty_dipesan

        # 5. Perhitungan Finansial Harian
        biaya_simpan = stok_akhir * config.biaya_simpan_per_hari
        biaya_pesan = config.biaya_pesan_per_order if pesan_hari_ini else 0.0
        biaya_stockout = lost_sales * biaya_stockout_unit
        total_biaya = biaya_simpan + biaya_pesan + biaya_stockout

        pendapatan = terjual * config.harga_jual
        cogs = terjual * config.harga_beli
        laba_kotor = pendapatan - cogs
        laba_bersih = laba_kotor - total_biaya

        status_stok = "Aman"
        if stok_akhir == 0:
            status_stok = "Habis (Stockout)"
        elif stok_akhir <= config.safety_stock:
            status_stok = "Di Bawah Safety Stock"

        log_harian.append({
            "Hari": hari,
            "Stok Awal": stok_awal_hari,
            "Pesanan Masuk": pesanan_tiba,
            "Stok Tersedia": stok_setelah_terima,
            "Permintaan": demand,
            "Penjualan": terjual,
            "Lost Sales": lost_sales,
            "Stok Akhir": stok_akhir,
            "Status Stok": status_stok,
            "Posisi Persediaan": posisi_persediaan,
            "Pesanan Dibuat": "Ya" if pesan_hari_ini else "Tidak",
            "Qty Dipesan": qty_dipesan,
            "Lead Time": lead_time_hari if pesan_hari_ini else 0,
            "Biaya Simpan": biaya_simpan,
            "Biaya Pesan": biaya_pesan,
            "Biaya Stockout": biaya_stockout,
            "Total Biaya": total_biaya,
            "Pendapatan": pendapatan,
            "Laba": laba_bersih,
        })

    return pd.DataFrame(log_harian)


def jalankan_monte_carlo(
    config: SimulationConfig
) -> Tuple[Dict[str, Any], pd.DataFrame, pd.DataFrame]:
    """
    Menjalankan simulasi Monte Carlo dengan R replikasi.
    
    Returns:
        ringkasan: Dict statistik rata-rata dan confidence interval
        df_replikasi: DataFrame hasil ringkasan per replikasi (untuk distribusi/histogram)
        df_detail_sample: DataFrame log harian dari replikasi pertama (untuk visualisasi run chart)
    """
    # Inisialisasi generator angka acak
    if config.random_seed is not None:
        rng_master = np.random.default_rng(config.random_seed)
    else:
        rng_master = np.random.default_rng()

    hasil_replikasi = []
    df_sample_detail = None

    for r in range(config.jumlah_replikasi):
        # Buat seed turunan unik untuk tiap replikasi
        rep_seed = rng_master.integers(0, 2**31 - 1)
        rng_rep = np.random.default_rng(rep_seed)

        df_rep = simulasi_satu_replikasi(config, rng_rep)

        if r == 0:
            df_sample_detail = df_rep.copy()

        # Hitung agregasi per replikasi
        total_permintaan = df_rep["Permintaan"].sum()
        total_penjualan = df_rep["Penjualan"].sum()
        total_lost_sales = df_rep["Lost Sales"].sum()
        service_level = (total_penjualan / total_permintaan * 100.0) if total_permintaan > 0 else 100.0
        hari_stockout = (df_rep["Stok Akhir"] == 0).sum()
        rata_stok = df_rep["Stok Akhir"].mean()
        frekuensi_pesanan = (df_rep["Pesanan Dibuat"] == "Ya").sum()

        total_biaya_simpan = df_rep["Biaya Simpan"].sum()
        total_biaya_pesan = df_rep["Biaya Pesan"].sum()
        total_biaya_stockout = df_rep["Biaya Stockout"].sum()
        total_biaya = df_rep["Total Biaya"].sum()
        total_pendapatan = df_rep["Pendapatan"].sum()
        total_laba = df_rep["Laba"].sum()

        hasil_replikasi.append({
            "Replikasi": r + 1,
            "Service Level (%)": service_level,
            "Hari Stockout": hari_stockout,
            "Total Lost Sales": total_lost_sales,
            "Rata-rata Stok": rata_stok,
            "Frekuensi Pesanan": frekuensi_pesanan,
            "Total Biaya Simpan": total_biaya_simpan,
            "Total Biaya Pesan": total_biaya_pesan,
            "Total Biaya Stockout": total_biaya_stockout,
            "Total Biaya": total_biaya,
            "Total Pendapatan": total_pendapatan,
            "Total Laba": total_laba,
        })

    df_replikasi = pd.DataFrame(hasil_replikasi)

    # Hitung ringkasan rata-rata, standar deviasi, dan interval (percentile 5% - 95%)
    ringkasan = {
        "service_level_mean": float(df_replikasi["Service Level (%)"].mean()),
        "service_level_std": float(df_replikasi["Service Level (%)"].std()),
        "service_level_ci_low": float(np.percentile(df_replikasi["Service Level (%)"], 5)),
        "service_level_ci_high": float(np.percentile(df_replikasi["Service Level (%)"], 95)),

        "hari_stockout_mean": float(df_replikasi["Hari Stockout"].mean()),
        "hari_stockout_std": float(df_replikasi["Hari Stockout"].std()),
        "hari_stockout_max": int(df_replikasi["Hari Stockout"].max()),

        "lost_sales_mean": float(df_replikasi["Total Lost Sales"].mean()),
        "lost_sales_std": float(df_replikasi["Total Lost Sales"].std()),

        "rata_stok_mean": float(df_replikasi["Rata-rata Stok"].mean()),
        "rata_stok_std": float(df_replikasi["Rata-rata Stok"].std()),

        "frekuensi_pesanan_mean": float(df_replikasi["Frekuensi Pesanan"].mean()),

        "biaya_simpan_mean": float(df_replikasi["Total Biaya Simpan"].mean()),
        "biaya_pesan_mean": float(df_replikasi["Total Biaya Pesan"].mean()),
        "biaya_stockout_mean": float(df_replikasi["Total Biaya Stockout"].mean()),
        "total_biaya_mean": float(df_replikasi["Total Biaya"].mean()),
        "total_biaya_std": float(df_replikasi["Total Biaya"].std()),
        "total_biaya_ci_low": float(np.percentile(df_replikasi["Total Biaya"], 5)),
        "total_biaya_ci_high": float(np.percentile(df_replikasi["Total Biaya"], 95)),

        "pendapatan_mean": float(df_replikasi["Total Pendapatan"].mean()),
        "laba_mean": float(df_replikasi["Total Laba"].mean()),
        "laba_std": float(df_replikasi["Total Laba"].std()),
        "laba_ci_low": float(np.percentile(df_replikasi["Total Laba"], 5)),
        "laba_ci_high": float(np.percentile(df_replikasi["Total Laba"], 95)),
    }

    return ringkasan, df_replikasi, df_sample_detail

