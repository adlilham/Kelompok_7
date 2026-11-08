"""
app.py - Aplikasi Web Simulasi Persediaan & Decision Support System (DSS)
Toko Buku "Cardinal"
Mata Kuliah: Teknik Simulasi dan Pemodelan
Tech Stack: Python 3.10+, Streamlit, NumPy, Pandas, Plotly
"""

import os
from datetime import datetime
from typing import Dict, Any, List
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from simulation import SimulationConfig, jalankan_monte_carlo, simulasi_satu_replikasi
from scenarios import (
    dapatkan_skenario_default,
    jalankan_analisis_skenario,
    berikan_rekomendasi_keputusan,
)

# ═══════════════════════════════════════════════════════════════════════════════
#  KONFIGURASI HALAMAN
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Simulasi Persediaan Stok Toko Buku Cardinal",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PRESET KATEGORI BUKU
# ═══════════════════════════════════════════════════════════════════════════════
PRESET_KATEGORI = {
    "Buku Umum": {
        "stok_awal": 100,
        "rata_permintaan": 8.0,
        "std_permintaan": 2.5,
        "lead_time_min": 2,
        "lead_time_max": 5,
        "rop": 30,
        "q": 80,
        "safety_stock": 10,
        "harga_beli": 50000.0,
        "harga_jual": 75000.0,
        "biaya_simpan": 200.0,
        "biaya_pesan": 100000.0,
        "deskripsi": "Koleksi buku populer & non-fiksi umum dengan permintaan stabil harian.",
    },
    "Novel & Fiksi": {
        "stok_awal": 80,
        "rata_permintaan": 6.0,
        "std_permintaan": 2.0,
        "lead_time_min": 3,
        "lead_time_max": 6,
        "rop": 25,
        "q": 60,
        "safety_stock": 8,
        "harga_beli": 60000.0,
        "harga_jual": 90000.0,
        "biaya_simpan": 250.0,
        "biaya_pesan": 120000.0,
        "deskripsi": "Novel sastra dan fiksi remaja dengan lead time penerbit yang lebih panjang.",
    },
    "Buku Pelajaran": {
        "stok_awal": 150,
        "rata_permintaan": 15.0,
        "std_permintaan": 4.0,
        "lead_time_min": 2,
        "lead_time_max": 4,
        "rop": 50,
        "q": 120,
        "safety_stock": 20,
        "harga_beli": 40000.0,
        "harga_jual": 60000.0,
        "biaya_simpan": 150.0,
        "biaya_pesan": 80000.0,
        "deskripsi": "Buku teks sekolah & kuliah ber-volume tinggi dengan distributor cepat tanggap.",
    },
    "Buku Anak": {
        "stok_awal": 70,
        "rata_permintaan": 5.0,
        "std_permintaan": 1.8,
        "lead_time_min": 2,
        "lead_time_max": 5,
        "rop": 20,
        "q": 50,
        "safety_stock": 10,
        "harga_beli": 35000.0,
        "harga_jual": 55000.0,
        "biaya_simpan": 180.0,
        "biaya_pesan": 90000.0,
        "deskripsi": "Buku bergambar dan mewarnai untuk anak-anak dengan ukuran fisik bervariasi.",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
#  INISIALISASI STATE SESSION & SINKRONISASI KATEGORI
# ═══════════════════════════════════════════════════════════════════════════════
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Buku Umum"

def terapkan_preset_ke_state(nama_kategori: str):
    """Menyinkronkan seluruh nilai input di session_state saat kategori berubah."""
    p = PRESET_KATEGORI[nama_kategori]
    # State nilai internal
    st.session_state.val_rop = p["rop"]
    st.session_state.val_q = p["q"]
    st.session_state.val_stok_awal = p["stok_awal"]
    st.session_state.val_safety_stock = p["safety_stock"]
    st.session_state.val_rata_permintaan = float(p["rata_permintaan"])
    st.session_state.val_std_permintaan = float(p["std_permintaan"])
    st.session_state.val_lt_min = p["lead_time_min"]
    st.session_state.val_lt_max = p["lead_time_max"]
    st.session_state.val_harga_beli = float(p["harga_beli"])
    st.session_state.val_harga_jual = float(p["harga_jual"])
    st.session_state.val_biaya_simpan = float(p["biaya_simpan"])
    st.session_state.val_biaya_pesan = float(p["biaya_pesan"])

    # Sinkronisasi langsung ke key widget Streamlit jika sudah aktif
    st.session_state["input_rop"] = p["rop"]
    st.session_state["input_q"] = p["q"]
    st.session_state["input_stok_awal"] = p["stok_awal"]
    st.session_state["input_ss"] = p["safety_stock"]
    st.session_state["input_rata_permintaan"] = float(p["rata_permintaan"])
    st.session_state["input_std_permintaan"] = float(p["std_permintaan"])
    st.session_state["input_lt_min"] = p["lead_time_min"]
    st.session_state["input_lt_max"] = p["lead_time_max"]
    st.session_state["input_harga_beli"] = float(p["harga_beli"])
    st.session_state["input_harga_jual"] = float(p["harga_jual"])
    st.session_state["input_biaya_simpan"] = float(p["biaya_simpan"])
    st.session_state["input_biaya_pesan"] = float(p["biaya_pesan"])

if "val_rop" not in st.session_state:
    terapkan_preset_ke_state(st.session_state.selected_category)

if "custom_scenarios" not in st.session_state:
    st.session_state.custom_scenarios = dapatkan_skenario_default()

# ═══════════════════════════════════════════════════════════════════════════════
#  CSS: UKURAN FONT JELAS, BESAR, RESPONSIF, RAMAH PANDANGAN MATA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global Font Scale (Teks Jauh Lebih Besar & Jelas Terbaca) */
html, body, [class*="css"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 18px !important; /* Ditingkatkan dari 15px ke 18px untuk kenyamanan mata */
}

/* Headings Standar */
h1 { font-size: 2.4rem !important; font-weight: 800 !important; }
h2 { font-size: 2.0rem !important; font-weight: 800 !important; }
h3 { font-size: 1.6rem !important; font-weight: 700 !important; }
h4 { font-size: 1.35rem !important; font-weight: 700 !important; }
p, li, span, div { font-size: 1.15rem; }

/* Tab Navigation Styling (Besar, Jelas & Berkontras Tinggi) */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: #0f1d22;
    padding: 10px 14px;
    border-radius: 14px;
    border: 1.5px solid rgba(255, 255, 255, 0.15);
    margin-bottom: 24px;
}
.stTabs [data-baseweb="tab"] {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    padding: 14px 24px !important;
    border-radius: 10px !important;
    color: #cbd5e1 !important;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.08) !important;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(0, 223, 130, 0.22) !important;
    color: #00df82 !important;
    border: 1.5px solid #00df82 !important;
    box-shadow: 0 4px 15px rgba(0, 223, 130, 0.25);
}

/* Header Banner */
.hero-card {
    background: linear-gradient(135deg, #0e2026 0%, #162f38 60%, #0d1a1f 100%);
    border: 2px solid rgba(0, 223, 130, 0.4);
    border-radius: 18px;
    padding: 26px 32px;
    margin-bottom: 26px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
}
.hero-title {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    gap: 14px;
}
.hero-badge {
    background: rgba(0, 223, 130, 0.2);
    border: 1.5px solid #00df82;
    color: #00df82;
    font-size: 1.05rem;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 20px;
    letter-spacing: 0.04em;
}
.hero-desc {
    color: #e2e8f0 !important;
    font-size: 1.25rem !important;
    line-height: 1.65 !important;
    margin-top: 12px !important;
    margin-bottom: 0px !important;
}

/* Kartu Informasi & Kotak Deskripsi */
.info-card {
    background: #112228;
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 24px 26px;
    margin-bottom: 22px;
}
.info-title {
    color: #00df82;
    font-size: 1.45rem;
    font-weight: 800;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.info-text {
    color: #e2e8f0;
    font-size: 1.18rem;
    line-height: 1.7;
    margin-bottom: 12px;
}

/* Box Formula Matematis */
.formula-box {
    background: #091316;
    border: 1.5px solid rgba(34, 211, 238, 0.4);
    border-radius: 12px;
    padding: 16px 22px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    color: #22d3ee;
    line-height: 1.8;
    margin: 14px 0;
}

/* Metric KPI Cards (Angka Besar & Jelas) */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 18px;
    margin-bottom: 26px;
}
.kpi-card {
    background: #102127;
    border: 1.5px solid rgba(255, 255, 255, 0.14);
    border-radius: 16px;
    padding: 20px 22px;
    transition: all 0.2s ease;
}
.kpi-card:hover {
    border-color: #00df82;
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.45);
}
.kpi-title {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}
.kpi-value {
    color: #ffffff;
    font-size: 2.5rem;
    font-weight: 900;
    margin: 0;
    line-height: 1.15;
}
.kpi-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 8px;
}

/* Callout Kotak Rekomendasi DSS */
.rekomendasi-card {
    background: linear-gradient(135deg, rgba(0, 223, 130, 0.15) 0%, rgba(14, 32, 38, 0.98) 100%);
    border: 2.5px solid #00df82;
    border-radius: 18px;
    padding: 30px 34px;
    margin-bottom: 26px;
    box-shadow: 0 12px 35px rgba(0, 223, 130, 0.2);
}
.rekomendasi-card.warning {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(32, 25, 14, 0.98) 100%);
    border-color: #f59e0b;
    box-shadow: 0 12px 35px rgba(245, 158, 11, 0.2);
}
.rekomendasi-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #00df82;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.rekomendasi-card.warning .rekomendasi-title {
    color: #f59e0b;
}
.rekomendasi-headline {
    font-size: 1.45rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 18px;
    line-height: 1.5;
}

/* Alur Proses Interaktif (Workflow Pipeline) */
.pipeline-flow {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
    margin: 20px 0;
}
.pipe-step {
    background: #112228;
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 20px;
}
.pipe-badge {
    display: inline-block;
    background: #00df82;
    color: #0a171a;
    font-weight: 800;
    font-size: 0.92rem;
    padding: 3px 10px;
    border-radius: 12px;
    margin-bottom: 10px;
}
.pipe-header {
    font-weight: 800;
    font-size: 1.25rem;
    color: #ffffff;
    margin-bottom: 8px;
}
.pipe-body {
    font-size: 1.1rem;
    color: #cbd5e1;
    line-height: 1.6;
}

/* Sidebar label & input styling */
label, .stWidgetLabel p {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}
.stNumberInput input, .stSelectbox div {
    font-size: 1.15rem !important;
}
.stSlider {
    font-size: 1.15rem !important;
}

/* Dataframe font scaling */
[data-testid="stDataFrame"] {
    font-size: 1.05rem !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  FUNGSI HELPER FORMAT RUPIAH & PLOTLY THEME
# ═══════════════════════════════════════════════════════════════════════════════
def format_rupiah(nilai: float) -> str:
    """Format angka float ke string Rupiah berpemisah ribuan."""
    return f"Rp {nilai:,.0f}".replace(",", ".")


def apply_plotly_theme(fig: go.Figure, height: int = 490) -> go.Figure:
    """Menerapkan styling dark modern dengan ukuran teks yang terbaca jelas."""
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0e1a1f",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#cbd5e1", size=15),
        title=dict(font=dict(size=18, color="#ffffff")),
        margin=dict(l=60, r=35, t=65, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=14, color="#cbd5e1"),
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#13242a",
            bordercolor="#00df82",
            font=dict(size=14, color="#ffffff", family="Plus Jakarta Sans"),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.08)",
        zeroline=False,
        tickfont=dict(size=14, color="#94a3b8"),
        title_font=dict(size=15, color="#e2e8f0"),
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.08)",
        zeroline=False,
        tickfont=dict(size=14, color="#94a3b8"),
        title_font=dict(size=15, color="#e2e8f0"),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR: PARAMETER INPUT
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📚 Parameter Toko Cardinal")
    st.caption("Pusat Pengaturan Parameter Persediaan & Biaya")

    # Dropdown Kategori Buku dengan sinkronisasi otomatis
    def on_category_change():
        terapkan_preset_ke_state(st.session_state.selected_category)

    kategori_terpilih = st.selectbox(
        "Kategori Judul Buku",
        options=list(PRESET_KATEGORI.keys()),
        key="selected_category",
        on_change=on_category_change,
        help="Memilih kategori otomatis menyesuaikan nilai default ROP, pesanan, dan biaya.",
    )
    preset = PRESET_KATEGORI[kategori_terpilih]
    st.info(f"📌 *{preset['deskripsi']}*")

    # Tombol Reset ke Default
    if st.button("🔄 Reset ke Nilai Default Kategori", width="stretch"):
        terapkan_preset_ke_state(kategori_terpilih)
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ Kebijakan Persediaan (s, Q)")

    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        reorder_point = st.number_input(
            "Reorder Point (s)",
            min_value=1,
            max_value=500,
            value=int(st.session_state.val_rop),
            step=5,
            key="input_rop",
            help="Batas stok di mana pesanan baru ke penerbit harus diterbitkan.",
        )
    with col_sb2:
        order_quantity = st.number_input(
            "Order Qty (Q)",
            min_value=1,
            max_value=1000,
            value=int(st.session_state.val_q),
            step=10,
            key="input_q",
            help="Banyaknya buku yang dipesan ke penerbit setiap pemesanan.",
        )

    col_sb3, col_sb4 = st.columns(2)
    with col_sb3:
        stok_awal = st.number_input(
            "Stok Awal (buku)",
            min_value=0,
            max_value=2000,
            value=int(st.session_state.val_stok_awal),
            step=10,
            key="input_stok_awal",
        )
    with col_sb4:
        safety_stock = st.number_input(
            "Safety Stock",
            min_value=0,
            max_value=200,
            value=int(st.session_state.val_safety_stock),
            step=5,
            key="input_ss",
            help="Batas aman stok penyangga untuk indikator kewaspadaan toko.",
        )

    st.markdown("---")
    st.markdown("### 🎲 Permintaan & Lead Time")

    distribusi_pilihan = st.selectbox(
        "Distribusi Permintaan Harian",
        options=["Poisson", "Normal"],
        index=0,
        help="Poisson cocok untuk kedatangan buku diskrit harian. Normal sebagai alternatif kontinu.",
    )

    rata_permintaan = st.number_input(
        "Rata-rata Permintaan / Hari",
        min_value=0.5,
        max_value=100.0,
        value=float(st.session_state.val_rata_permintaan),
        step=0.5,
        key="input_rata_permintaan",
    )

    std_permintaan = 2.5
    if distribusi_pilihan == "Normal":
        std_permintaan = st.number_input(
            "Standar Deviasi Permintaan",
            min_value=0.1,
            max_value=50.0,
            value=float(st.session_state.val_std_permintaan),
            step=0.5,
            key="input_std_permintaan",
        )

    lead_mode = st.radio(
        "Variasi Lead Time (Waktu Tunggu)",
        options=["Acak (Min - Max)", "Tetap"],
        horizontal=True,
    )
    mode_lt = "Acak" if "Acak" in lead_mode else "Tetap"

    col_lt1, col_lt2 = st.columns(2)
    with col_lt1:
        lt_min = st.number_input(
            "Lead Time Min (hari)",
            min_value=1,
            max_value=30,
            value=int(st.session_state.val_lt_min),
            step=1,
            key="input_lt_min",
        )
    with col_lt2:
        lt_max = st.number_input(
            "Lead Time Max (hari)",
            min_value=1,
            max_value=30,
            value=int(st.session_state.val_lt_max),
            step=1,
            key="input_lt_max",
        )

    if lt_min > lt_max:
        st.warning("⚠️ Lead Time Min melebihi Max. Nilai disesuaikan otomatis.")
        lt_max = lt_min

    st.markdown("---")
    st.markdown("### 💰 Parameter Finansial (Rp)")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        harga_beli = st.number_input(
            "Harga Beli / Buku",
            min_value=1000.0,
            max_value=1000000.0,
            value=float(st.session_state.val_harga_beli),
            step=5000.0,
            format="%.0f",
            key="input_harga_beli",
        )
    with col_f2:
        harga_jual = st.number_input(
            "Harga Jual / Buku",
            min_value=1000.0,
            max_value=1500000.0,
            value=float(st.session_state.val_harga_jual),
            step=5000.0,
            format="%.0f",
            key="input_harga_jual",
        )

    margin_default = max(0.0, harga_jual - harga_beli)

    biaya_simpan = st.number_input(
        "Biaya Simpan / Buku / Hari (Rp)",
        min_value=0.0,
        max_value=5000.0,
        value=float(st.session_state.val_biaya_simpan),
        step=50.0,
        format="%.0f",
        key="input_biaya_simpan",
    )

    biaya_pesan = st.number_input(
        "Biaya Pesan / Kali Pesan (Rp)",
        min_value=0.0,
        max_value=1000000.0,
        value=float(st.session_state.val_biaya_pesan),
        step=10000.0,
        format="%.0f",
        key="input_biaya_pesan",
    )

    opsi_stockout = st.checkbox(
        "Gunakan Margin Laba Sebagai Biaya Stockout",
        value=True,
        help=f"Biaya stockout per buku otomatis diisi {format_rupiah(margin_default)} (laba penjualan yang hilang).",
    )

    if opsi_stockout:
        biaya_stockout = margin_default
        st.caption(f"Biaya Kehabisan Stok: **{format_rupiah(biaya_stockout)}** / buku")
    else:
        biaya_stockout = st.number_input(
            "Biaya Kehabisan Stok / Buku (Rp)",
            min_value=0.0,
            max_value=500000.0,
            value=margin_default,
            step=5000.0,
            format="%.0f",
        )

    st.markdown("---")
    st.markdown("### ⏱️ Pengaturan Monte Carlo")

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        lama_simulasi = st.number_input(
            "Periode (Hari)",
            min_value=10,
            max_value=365,
            value=90,
            step=10,
        )
    with col_sim2:
        replikasi = st.number_input(
            "Replikasi",
            min_value=10,
            max_value=500,
            value=100,
            step=10,
        )

    use_seed = st.checkbox("Gunakan Random Seed Tetap", value=True)
    seed_val = 42 if use_seed else None
    if use_seed:
        seed_val = st.number_input("Nilai Seed", min_value=1, max_value=999999, value=42, step=1)

# Inisialisasi Objek Konfigurasi Simulasi
config_aktif = SimulationConfig(
    reorder_point=int(reorder_point),
    order_quantity=int(order_quantity),
    safety_stock=int(safety_stock),
    stok_awal=int(stok_awal),
    distribusi_permintaan=distribusi_pilihan,
    rata_permintaan=float(rata_permintaan),
    std_permintaan=float(std_permintaan),
    lead_time_min=int(lt_min),
    lead_time_max=int(lt_max),
    lead_time_mode=mode_lt,
    periode_hari=int(lama_simulasi),
    jumlah_replikasi=int(replikasi),
    random_seed=seed_val,
    harga_beli=float(harga_beli),
    harga_jual=float(harga_jual),
    biaya_simpan_per_hari=float(biaya_simpan),
    biaya_pesan_per_order=float(biaya_pesan),
    biaya_stockout_per_unit=float(biaya_stockout),
)

# ═══════════════════════════════════════════════════════════════════════════════
#  CACHED SIMULATION EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def jalankan_simulasi_tercache(cfg: SimulationConfig):
    """Menjalankan Monte Carlo dengan caching Streamlit untuk efisiensi komputasi."""
    return jalankan_monte_carlo(cfg)


@st.cache_data(show_spinner=False)
def jalankan_skenario_tercache(daftar_skenario_tuple, cfg: SimulationConfig):
    """Menjalankan batch skenario dengan caching."""
    daftar = [dict(s) for s in daftar_skenario_tuple]
    return jalankan_analisis_skenario(daftar, cfg)


# ═══════════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <h1 class="hero-title">
            <span>📚 Toko Buku Cardinal</span>
            <span class="hero-badge">Decision Support System</span>
        </h1>
        <span style="color: #00df82; font-size: 1.15rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">
            Teknik Simulasi dan Pemodelan
        </span>
    </div>
    <p class="hero-desc">
        Aplikasi simulasi Monte Carlo persediaan harian berbasis kebijakan <b>(s, Q)</b> untuk meminimalkan 
        risiko kehabisan stok (<i>stockout</i>) sekaligus menekan total biaya persediaan secara optimal.
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  5 TAB UTAMA (UKURAN TEKS BESAR, JELAS & MUDAH DINAVIGASI)
# ═══════════════════════════════════════════════════════════════════════════════
tab_beranda, tab_simulasi, tab_skenario, tab_rekomendasi, tab_unduh = st.tabs([
    "🏠 1. Beranda",
    "📊 2. Simulasi Tunggal",
    "🔄 3. Perbandingan Skenario",
    "💡 4. Rekomendasi Keputusan",
    "📥 5. Data dan Unduh",
])


# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 1: BERANDA
# ═══════════════════════════════════════════════════════════════════════════════
with tab_beranda:
    st.markdown("### 📖 Latar Belakang Studi Kasus")
    
    st.markdown("""
    <div class="info-card">
        <p class="info-text">
            <b>Toko Buku Cardinal</b> menjual buku dengan pola permintaan pembeli yang bervariasi setiap hari. 
            Tantangan mendasar yang dihadapi pemilik toko adalah menentukan <b>Kapan harus memesan kembali (<i>Reorder Point / s</i>)</b> 
            dan <b>Berapa banyak jumlah pesanan (<i>Order Quantity / Q</i>)</b> ke penerbit atau distributor.
        </p>
        <p class="info-text" style="margin-bottom: 0;">
            Jika stok terlalu sedikit, toko sering kehabisan persediaan (<i>stockout</i>) sehingga kehilangan potensi pembeli (<i>lost sales</i>). 
            Sebaliknya, jika menyetok terlalu banyak buku, biaya simpan di gudang akan membengkak dan mengunci modal kerja toko.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">🎯 Model Kebijakan Persediaan (s, Q)</div>
            <p class="info-text">
                Sistem mengadopsi model peninjauan harian kontinu <i>(s, Q) Continuous Review Policy</i>:
            </p>
            <div class="formula-box">
                Posisi Persediaan = Stok Fisik + Pesanan Dalam Pengiriman<br>
                Jika Posisi Persediaan ≤ s (Reorder Point):<br>
                &nbsp;&nbsp;&nbsp;&nbsp;Pesan sejumlah Q buku ke distributor
            </div>
            <ul style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.8; padding-left: 24px;">
                <li><b>Reorder Point (s)</b>: Titik batas ambang pemicu pemesanan kembali.</li>
                <li><b>Order Quantity (Q)</b>: Jumlah tetap unit buku yang dipesan ke penerbit.</li>
                <li><b>Lead Time (L)</b>: Jeda hari pengiriman sejak dipesan hingga buku tiba di toko.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">📐 Asumsi & Rumus Finansial</div>
            <p class="info-text">
                Evaluasi kinerja biaya dan profitabilitas operasional harian:
            </p>
            <div class="formula-box">
                Biaya Total = Biaya Simpan + Biaya Pesan + Biaya Stockout<br>
                Laba Bersih = Pendapatan - HPP - Biaya Total Operasional<br>
                Service Level (%) = (Total Terjual / Total Permintaan) × 100%
            </div>
            <ul style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.8; padding-left: 24px;">
                <li><b>Lost Sales</b>: Permintaan yang tidak terpenuhi hangus (tidak ada antrean <i>backorder</i>).</li>
                <li><b>Simulasi Monte Carlo</b>: Replikasi berulang (100 kali) untuk mendapatkan kestabilan statistik dan selang kepercayaan (CI).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔄 Alur Kerja Simulasi Harian (Day-by-Day Workflow)")
    
    # Render Workflow Pipeline native HTML
    st.markdown("""
    <div class="pipeline-flow">
        <div class="pipe-step">
            <span class="pipe-badge">Langkah 1</span>
            <div class="pipe-header">📦 Terima Barang Datang</div>
            <div class="pipe-body">Cek pesanan terdahulu yang jatuh tempo hari ini. Stok di rak bertambah sebesar kuantitas pesanan tiba.</div>
        </div>
        <div class="pipe-step">
            <span class="pipe-badge">Langkah 2</span>
            <div class="pipe-header">🎲 Bangkitkan Permintaan</div>
            <div class="pipe-body">Permintaan harian pelanggan dibangkitkan secara acak dari distribusi <b>Poisson</b> atau <b>Normal</b>.</div>
        </div>
        <div class="pipe-step">
            <span class="pipe-badge">Langkah 3</span>
            <div class="pipe-header">🛒 Penjualan & Lost Sales</div>
            <div class="pipe-body">Penjualan = min(Permintaan, Stok). Jika stok kurang, selisihnya dicatat sebagai penjualan hilang (<i>lost sales</i>).</div>
        </div>
        <div class="pipe-step">
            <span class="pipe-badge">Langkah 4</span>
            <div class="pipe-header">📊 Hitung Posisi Persediaan</div>
            <div class="pipe-body">Posisi Persediaan = Stok Akhir Fisik + Total Pesanan yang sedang dalam perjalanan pengiriman (<i>on-order</i>).</div>
        </div>
        <div class="pipe-step">
            <span class="pipe-badge">Langkah 5</span>
            <div class="pipe-header">🔔 Evaluasi Pemesanan (s, Q)</div>
            <div class="pipe-body">Jika Posisi Persediaan ≤ <b>s</b>, terbitkan Purchase Order sebesar <b>Q</b> buku dengan waktu tunggu <i>lead time</i> acak.</div>
        </div>
        <div class="pipe-step">
            <span class="pipe-badge">Langkah 6</span>
            <div class="pipe-header">💰 Akumulasi Biaya & Laba</div>
            <div class="pipe-body">Hitung biaya simpan, biaya pesan, biaya stockout, pendapatan kotor, serta estimasi laba bersih harian.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **Petunjuk Penggunaan**: Atur parameter persediaan dan biaya pada bilah kiri (Sidebar), kemudian telusuri **Tab 2** untuk melihat simulasi tunggal, **Tab 3** untuk perbandingan skenario, dan **Tab 4** untuk memperoleh rekomendasi waktu dan jumlah pemesanan terbaik.")


# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 2: SIMULASI TUNGGAL
# ═══════════════════════════════════════════════════════════════════════════════
with tab_simulasi:
    st.markdown(f"### 📊 Hasil Simulasi Tunggal — Kategori: {kategori_terpilih}")
    st.caption(
        f"Kebijakan Terpilih: **ROP (s) = {config_aktif.reorder_point} buku**, "
        f"**Order Qty (Q) = {config_aktif.order_quantity} buku**, "
        f"Lama Simulasi = {config_aktif.periode_hari} Hari ({config_aktif.jumlah_replikasi} Replikasi Monte Carlo)"
    )

    with st.spinner("Menjalankan simulasi Monte Carlo..."):
        ringkasan_tunggal, df_replikasi_tunggal, df_sample_tunggal = jalankan_simulasi_tercache(config_aktif)

    # ── KPI METRICS CARDS ──
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Service Level</div>
            <div class="kpi-value" style="color: {'#00df82' if ringkasan_tunggal['service_level_mean'] >= 95 else '#f59e0b'};">
                {ringkasan_tunggal['service_level_mean']:.2f}%
            </div>
            <div class="kpi-sub">Rentang CI 90%: {ringkasan_tunggal['service_level_ci_low']:.1f}% - {ringkasan_tunggal['service_level_ci_high']:.1f}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Hari Stockout</div>
            <div class="kpi-value" style="color: {'#f43f5e' if ringkasan_tunggal['hari_stockout_mean'] > 3 else '#38bdf8'};">
                {ringkasan_tunggal['hari_stockout_mean']:.1f} <span style="font-size:1.2rem; font-weight:normal; color:#94a3b8;">hari</span>
            </div>
            <div class="kpi-sub">Lost Sales: {ringkasan_tunggal['lost_sales_mean']:.1f} buku</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Rata-rata Stok di Tangan</div>
            <div class="kpi-value">
                {ringkasan_tunggal['rata_stok_mean']:.1f} <span style="font-size:1.2rem; font-weight:normal; color:#94a3b8;">buku</span>
            </div>
            <div class="kpi-sub">Frekuensi Pesan: {ringkasan_tunggal['frekuensi_pesanan_mean']:.1f} kali</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Biaya Operasional</div>
            <div class="kpi-value" style="color: #f59e0b;">
                {format_rupiah(ringkasan_tunggal['total_biaya_mean'])}
            </div>
            <div class="kpi-sub">Simpan + Pesan + Stockout</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Estimasi Laba Bersih</div>
            <div class="kpi-value" style="color: #00df82;">
                {format_rupiah(ringkasan_tunggal['laba_mean'])}
            </div>
            <div class="kpi-sub">Pendapatan Bersih Setelah Biaya</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── GRAFIK PERGERAKAN STOK HARIAN & DEMAND VS SALES ──
    st.markdown("#### 📈 Visualisasi Dinamika Persediaan Harian (Replikasi Sampel)")
    
    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        # 1. Line Chart: Pergerakan Stok
        fig_stock = go.Figure()

        # Garis Stok Akhir
        fig_stock.add_trace(go.Scatter(
            x=df_sample_tunggal["Hari"],
            y=df_sample_tunggal["Stok Akhir"],
            mode="lines+markers",
            name="Stok Akhir Fisik",
            line=dict(color="#00df82", width=3),
            marker=dict(size=5),
            hovertemplate="Hari %{x}<br>Stok Akhir: %{y} buku<extra></extra>",
        ))

        # Garis Posisi Persediaan
        fig_stock.add_trace(go.Scatter(
            x=df_sample_tunggal["Hari"],
            y=df_sample_tunggal["Posisi Persediaan"],
            mode="lines",
            name="Posisi Persediaan (On-Hand + On-Order)",
            line=dict(color="#38bdf8", width=2, dash="dash"),
            hovertemplate="Hari %{x}<br>Posisi Persediaan: %{y} buku<extra></extra>",
        ))

        # Garis Reorder Point
        fig_stock.add_trace(go.Scatter(
            x=[1, config_aktif.periode_hari],
            y=[config_aktif.reorder_point, config_aktif.reorder_point],
            mode="lines",
            name=f"Reorder Point (s = {config_aktif.reorder_point})",
            line=dict(color="#f59e0b", width=2.5, dash="dot"),
        ))

        # Garis Safety Stock
        fig_stock.add_trace(go.Scatter(
            x=[1, config_aktif.periode_hari],
            y=[config_aktif.safety_stock, config_aktif.safety_stock],
            mode="lines",
            name=f"Safety Stock ({config_aktif.safety_stock})",
            line=dict(color="#f43f5e", width=2, dash="dot"),
        ))

        # Titik Pemesanan Baru Dibuat
        order_days = df_sample_tunggal[df_sample_tunggal["Pesanan Dibuat"] == "Ya"]
        if not order_days.empty:
            fig_stock.add_trace(go.Scatter(
                x=order_days["Hari"],
                y=order_days["Stok Akhir"],
                mode="markers",
                name="Pesanan Dibuat (Q)",
                marker=dict(symbol="triangle-up", size=13, color="#f59e0b", line=dict(width=1.5, color="#ffffff")),
                hovertemplate="Hari %{x}: Pesan %{text} buku<extra></extra>",
                text=order_days["Qty Dipesan"],
            ))

        fig_stock.update_layout(
            title="Pergerakan Stok Harian vs Reorder Point (s) & Safety Stock",
            xaxis_title="Hari ke-",
            yaxis_title="Kuantitas Buku (Unit)",
        )
        st.plotly_chart(apply_plotly_theme(fig_stock, height=460), width="stretch")

    with col_g2:
        # 2. Grafik Komposisi Biaya (Donut Chart)
        biaya_labels = ["Biaya Simpan", "Biaya Pesan", "Biaya Stockout"]
        biaya_values = [
            ringkasan_tunggal["biaya_simpan_mean"],
            ringkasan_tunggal["biaya_pesan_mean"],
            ringkasan_tunggal["biaya_stockout_mean"],
        ]
        biaya_colors = ["#22d3ee", "#f59e0b", "#f43f5e"]

        fig_pie = go.Figure(data=[go.Pie(
            labels=biaya_labels,
            values=biaya_values,
            hole=0.55,
            marker=dict(colors=biaya_colors),
            textinfo="label+percent",
            textfont=dict(size=15),
            hovertemplate="%{label}: Rp %{value:,.0f}<br>(%{percent})<extra></extra>",
        )])
        fig_pie.update_layout(
            title="Komposisi Rata-rata Biaya Operasional",
            showlegend=False,
        )
        st.plotly_chart(apply_plotly_theme(fig_pie, height=460), width="stretch")

    # ── BAR CHART DEMAND VS SALES & HISTOGRAM REPLIKASI ──
    col_g3, col_g4 = st.columns(2)

    with col_g3:
        # Bar chart: Permintaan vs Penjualan vs Lost Sales
        fig_demand = go.Figure()
        fig_demand.add_trace(go.Bar(
            x=df_sample_tunggal["Hari"],
            y=df_sample_tunggal["Penjualan"],
            name="Penjualan Terpenuhi",
            marker_color="#00df82",
        ))
        fig_demand.add_trace(go.Bar(
            x=df_sample_tunggal["Hari"],
            y=df_sample_tunggal["Lost Sales"],
            name="Lost Sales (Kehabisan Stok)",
            marker_color="#f43f5e",
        ))
        fig_demand.update_layout(
            barmode="stack",
            title="Permintaan Harian vs Penjualan Terpenuhi & Lost Sales",
            xaxis_title="Hari ke-",
            yaxis_title="Kuantitas Buku (Unit)",
        )
        st.plotly_chart(apply_plotly_theme(fig_demand, height=420), width="stretch")

    with col_g4:
        # Histogram Sebaran Service Level & Total Biaya
        fig_dist = make_subplots(rows=1, cols=2, subplot_titles=("Sebaran Service Level (%)", "Sebaran Total Biaya (Rp)"))
        
        # Hist Service Level
        fig_dist.add_trace(
            go.Histogram(
                x=df_replikasi_tunggal["Service Level (%)"],
                nbinsx=15,
                name="Service Level",
                marker_color="#00df82",
                opacity=0.85,
            ),
            row=1, col=1
        )
        # Hist Total Biaya
        fig_dist.add_trace(
            go.Histogram(
                x=df_replikasi_tunggal["Total Biaya"],
                nbinsx=15,
                name="Total Biaya",
                marker_color="#f59e0b",
                opacity=0.85,
            ),
            row=1, col=2
        )
        fig_dist.update_layout(
            title=f"Distribusi Hasil dari Seluruh {config_aktif.jumlah_replikasi} Replikasi Monte Carlo",
            showlegend=False,
        )
        st.plotly_chart(apply_plotly_theme(fig_dist, height=420), width="stretch")

    # ── TABEL LOG SIMULASI HARIAN ──
    st.markdown("#### 📋 Log Simulasi Harian (Sampel Replikasi 1)")
    with st.expander("Buka / Tutup Tabel Rincian Data Harian", expanded=False):
        df_display_log = df_sample_tunggal.copy()
        
        # Format angka rupiah untuk tampilan tabel
        for col_biaya in ["Biaya Simpan", "Biaya Pesan", "Biaya Stockout", "Total Biaya", "Pendapatan", "Laba"]:
            df_display_log[col_biaya] = df_display_log[col_biaya].apply(lambda v: f"Rp {v:,.0f}".replace(",", "."))
        
        st.dataframe(
            df_display_log,
            width="stretch",
            height=380,
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 3: PERBANDINGAN SKENARIO
# ═══════════════════════════════════════════════════════════════════════════════
with tab_skenario:
    st.markdown("### 🔄 Perbandingan Berbagai Skenario Kebijakan (s, Q)")
    st.caption("Uji coba serentak berbagai kombinasi Reorder Point dan Order Quantity untuk menemukan trade-off optimal.")

    # ── FORM TAMBAH SKENARIO KUSTOM ──
    with st.expander("➕ Tambah Skenario Kustom Baru", expanded=False):
        col_ks1, col_ks2, col_ks3, col_ks4 = st.columns([3, 2, 2, 2])
        with col_ks1:
            nama_baru = st.text_input("Nama Skenario", value=f"Skenario Kustom {len(st.session_state.custom_scenarios) + 1}")
        with col_ks2:
            rop_baru = st.number_input("ROP (s)", min_value=5, max_value=300, value=35, step=5)
        with col_ks3:
            q_baru = st.number_input("Order Qty (Q)", min_value=10, max_value=500, value=90, step=10)
        with col_ks4:
            st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
            if st.button("Simpan Skenario", type="primary", width="stretch"):
                st.session_state.custom_scenarios.append({
                    "id": len(st.session_state.custom_scenarios) + 1,
                    "nama": nama_baru,
                    "rop": int(rop_baru),
                    "q": int(q_baru),
                    "deskripsi": f"Skenario kustom pengguna dengan ROP {rop_baru} dan Qty {q_baru}",
                })
                st.success(f"Skenario '{nama_baru}' berhasil ditambahkan!")
                st.rerun()

        # Daftar skenario kustom yang dapat dihapus individual
        if len(st.session_state.custom_scenarios) > 4:
            st.markdown("---")
            st.markdown("##### 🗑️ Kelola / Hapus Skenario Kustom")
            for idx in range(4, len(st.session_state.custom_scenarios)):
                sk = st.session_state.custom_scenarios[idx]
                col_d_info, col_d_btn = st.columns([5, 1])
                with col_d_info:
                    st.write(f"• **{sk['nama']}** — ROP: {sk['rop']}, Q: {sk['q']}")
                with col_d_btn:
                    if st.button("Hapus", key=f"del_sc_{idx}"):
                        st.session_state.custom_scenarios.pop(idx)
                        st.rerun()

    # Tombol Reset Skenario ke Default
    col_info, col_reset = st.columns([5, 1])
    with col_info:
        st.write(f"Menjalankan simulasi untuk **{len(st.session_state.custom_scenarios)} skenario kebijakan** secara serentak:")
    with col_reset:
        if st.button("Reset Skenario", help="Kembalikan daftar skenario ke 4 skenario default"):
            st.session_state.custom_scenarios = dapatkan_skenario_default()
            st.rerun()

    # Eksekusi Analisis Skenario
    tuple_skenarios = tuple(tuple(d.items()) for d in st.session_state.custom_scenarios)
    with st.spinner("Menjalankan simulasi Monte Carlo untuk semua skenario..."):
        df_skenario_hasil, dict_rep_skenario = jalankan_skenario_tercache(tuple_skenarios, config_aktif)

    # ── TABEL PERBANDINGAN SKENARIO ──
    df_tampil_skenario = df_skenario_hasil.copy()
    
    # Format kolom numerik untuk tampilan
    kolom_rupiah = ["Biaya Simpan (Rp)", "Biaya Pesan (Rp)", "Biaya Stockout (Rp)", "Total Biaya (Rp)", "Estimasi Laba (Rp)"]
    for k in kolom_rupiah:
        df_tampil_skenario[k] = df_tampil_skenario[k].apply(lambda v: f"Rp {v:,.0f}".replace(",", "."))
    
    df_tampil_skenario["Service Level (%)"] = df_tampil_skenario["Service Level (%)"].apply(lambda v: f"{v:.2f}%")
    df_tampil_skenario["Hari Stockout"] = df_tampil_skenario["Hari Stockout"].apply(lambda v: f"{v:.1f} hari")
    df_tampil_skenario["Lost Sales (Buku)"] = df_tampil_skenario["Lost Sales (Buku)"].apply(lambda v: f"{v:.1f}")
    df_tampil_skenario["Rata-rata Stok"] = df_tampil_skenario["Rata-rata Stok"].apply(lambda v: f"{v:.1f}")
    df_tampil_skenario["Frekuensi Pesan"] = df_tampil_skenario["Frekuensi Pesan"].apply(lambda v: f"{v:.1f}x")

    st.dataframe(
        df_tampil_skenario[[
            "Skenario", "ROP (s)", "Order Qty (Q)", "Service Level (%)", 
            "Hari Stockout", "Lost Sales (Buku)", "Rata-rata Stok", "Frekuensi Pesan",
            "Total Biaya (Rp)", "Estimasi Laba (Rp)", "Deskripsi"
        ]],
        width="stretch",
        hide_index=True,
    )

    # ── GRAFIK KOMPARASI ──
    st.markdown("#### 📊 Grafik Komparasi Antar Skenario")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        # Bar Chart Total Biaya vs Laba
        fig_cost_profit = go.Figure()
        fig_cost_profit.add_trace(go.Bar(
            x=df_skenario_hasil["Skenario"],
            y=df_skenario_hasil["Total Biaya (Rp)"],
            name="Total Biaya Operasional",
            marker_color="#f59e0b",
            hovertemplate="%{x}<br>Total Biaya: Rp %{y:,.0f}<extra></extra>",
        ))
        fig_cost_profit.add_trace(go.Bar(
            x=df_skenario_hasil["Skenario"],
            y=df_skenario_hasil["Estimasi Laba (Rp)"],
            name="Estimasi Laba Bersih",
            marker_color="#00df82",
            hovertemplate="%{x}<br>Estimasi Laba: Rp %{y:,.0f}<extra></extra>",
        ))
        fig_cost_profit.update_layout(
            title="Perbandingan Total Biaya vs Estimasi Laba Bersih",
            barmode="group",
            xaxis_title="Kebijakan Skenario",
            yaxis_title="Nominal (Rp)",
        )
        st.plotly_chart(apply_plotly_theme(fig_cost_profit, height=450), width="stretch")

    with col_c2:
        # Bar Chart Service Level dengan Target Line
        fig_sl = go.Figure()
        fig_sl.add_trace(go.Bar(
            x=df_skenario_hasil["Skenario"],
            y=df_skenario_hasil["Service Level (%)"],
            name="Service Level",
            marker_color="#38bdf8",
            hovertemplate="%{x}<br>Service Level: %{y:.2f}%<extra></extra>",
        ))
        fig_sl.add_hline(
            y=95.0,
            line_dash="dot",
            line_color="#f43f5e",
            annotation_text="Target Standar (95%)",
            annotation_position="bottom right",
            annotation_font=dict(size=14, color="#f43f5e"),
        )
        fig_sl.update_layout(
            title="Capaian Service Level (%) per Skenario",
            xaxis_title="Kebijakan Skenario",
            yaxis_title="Service Level (%)",
            yaxis=dict(range=[70, 102]),
        )
        st.plotly_chart(apply_plotly_theme(fig_sl, height=450), width="stretch")

    # ── STACKED BAR BREAKDOWN BIAYA & SCATTER TRADE-OFF ──
    col_c3, col_c4 = st.columns(2)
    with col_c3:
        # Breakdown Biaya (Stacked Bar)
        fig_breakdown = go.Figure()
        fig_breakdown.add_trace(go.Bar(
            x=df_skenario_hasil["Skenario"],
            y=df_skenario_hasil["Biaya Simpan (Rp)"],
            name="Biaya Simpan",
            marker_color="#22d3ee",
        ))
        fig_breakdown.add_trace(go.Bar(
            x=df_skenario_hasil["Skenario"],
            y=df_skenario_hasil["Biaya Pesan (Rp)"],
            name="Biaya Pesan",
            marker_color="#f59e0b",
        ))
        fig_breakdown.add_trace(go.Bar(
            x=df_skenario_hasil["Skenario"],
            y=df_skenario_hasil["Biaya Stockout (Rp)"],
            name="Biaya Stockout (Lost Sales)",
            marker_color="#f43f5e",
        ))
        fig_breakdown.update_layout(
            title="Rincian Komponen Biaya Operasional per Skenario",
            barmode="stack",
            xaxis_title="Skenario",
            yaxis_title="Biaya (Rp)",
        )
        st.plotly_chart(apply_plotly_theme(fig_breakdown, height=450), width="stretch")

    with col_c4:
        # Scatter Trade-off: Service Level vs Total Biaya
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=df_skenario_hasil["Total Biaya (Rp)"],
            y=df_skenario_hasil["Service Level (%)"],
            mode="markers+text",
            text=df_skenario_hasil["Skenario"].apply(lambda s: s.split("(")[0].strip()),
            textposition="top center",
            textfont=dict(size=14, color="#ffffff"),
            marker=dict(
                size=df_skenario_hasil["Order Qty (Q)"] / 2.8,
                color=df_skenario_hasil["Estimasi Laba (Rp)"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Laba (Rp)"),
            ),
            hovertemplate="<b>%{text}</b><br>Biaya: Rp %{x:,.0f}<br>Service Level: %{y:.2f}%<extra></extra>",
        ))
        fig_scatter.update_layout(
            title="Trade-off: Service Level vs Total Biaya (Ukuran Titik = Qty Pesan)",
            xaxis_title="Total Biaya Operasional (Rp)",
            yaxis_title="Service Level (%)",
        )
        st.plotly_chart(apply_plotly_theme(fig_scatter, height=450), width="stretch")


# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 4: REKOMENDASI KEPUTUSAN (DECISION SUPPORT SYSTEM)
# ═══════════════════════════════════════════════════════════════════════════════
with tab_rekomendasi:
    st.markdown("### 💡 Sistem Pendukung Keputusan (Decision Support System)")
    st.caption("Analisis optimasi terotomatisasi untuk memilih waktu dan kuantitas pemesanan buku terbaik.")

    # Slider Target Service Level
    col_t1, col_t2 = st.columns([2, 3])
    with col_t1:
        target_sl = st.slider(
            "Target Minimal Service Level (%)",
            min_value=80.0,
            max_value=99.5,
            value=95.0,
            step=0.5,
            help="Batas minimum persentase permintaan pembeli yang wajib dapat dipenuhi toko tanpa mengalami stockout.",
        )
    with col_t2:
        st.markdown(f"""
        <div style="background: #112228; border-radius: 14px; padding: 18px 22px; border: 1.5px solid rgba(255,255,255,0.12); margin-top: 10px;">
            <div style="color: #94a3b8; font-size: 1.05rem; font-weight: 700;">Kriteria Seleksi DSS Toko Cardinal:</div>
            <div style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-top: 6px; line-height: 1.6;">
                1. Service Level ≥ <span style="color:#00df82;">{target_sl:.1f}%</span><br>
                2. Total Biaya Operasional Minimum (Laba Maksimal)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Hitung Rekomendasi
    rekomendasi = berikan_rekomendasi_keputusan(df_skenario_hasil, target_service_level=target_sl)

    # ── KOTAK REKOMENDASI UTAMA ──
    is_warning = rekomendasi["status"] == "PERINGATAN"
    card_class = "rekomendasi-card warning" if is_warning else "rekomendasi-card"
    badge_label = "⚠️ PERINGATAN / KONDISI KHUSUS" if is_warning else "🏆 REKOMENDASI KEBIJAKAN TERBAIK"

    # Format list alasan dalam tag HTML yang valid
    alasan_html = "".join(f"<li style='margin-bottom: 8px;'>{item}</li>" for item in rekomendasi["alasan"])

    st.markdown(f"""
    <div class="{card_class}">
        <div class="rekomendasi-title">
            <span>{badge_label}</span>
        </div>
        <div class="rekomendasi-headline">
            {rekomendasi['kalimat_utama']}
        </div>
        <div style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-bottom: 12px;">
            Alasan & Landasan Analisis Kuantitatif:
        </div>
        <ul style="color: #e2e8f0; font-size: 1.15rem; line-height: 1.8; margin-bottom: 20px; padding-left: 26px;">
            {alasan_html}
        </ul>
        <div style="background: rgba(0,0,0,0.35); border-radius: 10px; padding: 14px 18px; color: #cbd5e1; font-size: 1.15rem;">
            📌 <b>Catatan Manajerial:</b> {rekomendasi['catatan']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MATRIKS EVALUASI SELURUH SKENARIO ──
    st.markdown("#### 🔍 Matriks Evaluasi Kelayakan Seluruh Skenario")
    df_eval = pd.DataFrame(rekomendasi["evaluasi_semua"])
    df_eval_display = pd.DataFrame({
        "Skenario": df_eval["skenario"],
        "ROP (s)": df_eval["rop"],
        "Order Qty (Q)": df_eval["q"],
        "Capaian Service Level": df_eval["service_level"].apply(lambda v: f"{v:.2f}%"),
        "Target Status": df_eval["service_level"].apply(lambda v: "✅ Lolos" if v >= target_sl else "❌ Di Bawah Target"),
        "Total Biaya": df_eval["total_biaya"].apply(format_rupiah),
        "Estimasi Laba": df_eval["laba"].apply(format_rupiah),
        "Keputusan DSS": df_eval["status_label"],
        "Keterangan": df_eval["catatan"],
    })
    st.dataframe(df_eval_display, width="stretch", hide_index=True)

    # ── PANDUAN IMPLEMENTASI OPERASIONAL ──
    st.markdown("---")
    st.markdown("#### 📋 Panduan Eksekusi bagi Pemilik / Manajer Toko")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">📦 Standar Prosedur Operasional (SOP) Pemesanan</div>
            <ol style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.85; padding-left: 24px;">
                <li>Setiap penutupan toko di malam hari, hitung <b>Stok Fisik di Tangan</b>.</li>
                <li>Tambahkan dengan buku yang masih dalam status pengiriman distributor (<i>on-order</i>).</li>
                <li>Jika total <b>≤ {rekomendasi['rop']} buku</b>, terbitkan Purchase Order (PO) sebesar <b>{rekomendasi['q']} buku</b> ke distributor utama.</li>
                <li>Konfirmasi jadwal pengiriman distributor agar sesuai batas lead time {config_aktif.lead_time_min}-{config_aktif.lead_time_max} hari.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">🛡️ Strategi Manajemen Risiko Persediaan</div>
            <ul style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.85; padding-left: 24px;">
                <li><b>Lonjakan Musiman</b>: Menjelang tahun ajaran baru atau libur semester, tingkatkan ROP sebesar 15-20% untuk mengantisipasi lonjakan permintaan buku.</li>
                <li><b>Pencegahan Stockout</b>: Biaya kehilangan penjualan (margin laba) jauh lebih mahal daripada biaya simpan harian; jangan membiarkan stok mendekati nol.</li>
                <li><b>Evaluasi Berkala</b>: Lakukan peninjauan ulang parameter setiap bulan atau saat terjadi perubahan harga penerbit.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 5: DATA DAN UNDUH
# ═══════════════════════════════════════════════════════════════════════════════
with tab_unduh:
    st.markdown("### 📥 Unduh Data Hasil Simulasi & Eksperimen")
    st.caption("Ekspor data mentah dan ringkasan simulasi dalam format CSV untuk analisis lebih lanjut atau lampiran laporan/makalah.")

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    tab_d1, tab_d2, tab_d3, tab_d4 = st.tabs([
        "📄 1. Log Harian Simulasi Tunggal",
        "📑 2. Data Seluruh Replikasi Monte Carlo",
        "📊 3. Hasil Perbandingan Skenario",
        "📘 4. Dokumen Laporan Word (.docx)",
    ])

    with tab_d1:
        st.write("Data log harian simulasi tunggal (Replikasi ke-1, horizon 90 hari):")
        csv_daily = df_sample_tunggal.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Unduh Log Harian (CSV)",
            data=csv_daily,
            file_name=f"log_harian_toko_cardinal_{timestamp_str}.csv",
            mime="text/csv",
            type="primary",
        )
        st.dataframe(df_sample_tunggal, width="stretch", height=380)

    with tab_d2:
        st.write(f"Rangkuman metrik dari total {config_aktif.jumlah_replikasi} replikasi Monte Carlo:")
        csv_rep = df_replikasi_tunggal.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Unduh Data Replikasi Monte Carlo (CSV)",
            data=csv_rep,
            file_name=f"replikasi_monte_carlo_{timestamp_str}.csv",
            mime="text/csv",
            type="primary",
        )
        st.dataframe(df_replikasi_tunggal, width="stretch", height=380)

    with tab_d3:
        st.write("Data komparasi seluruh skenario kebijakan persediaan (s, Q):")
        csv_scenarios = df_skenario_hasil.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Unduh Hasil Perbandingan Skenario (CSV)",
            data=csv_scenarios,
            file_name=f"perbandingan_skenario_cardinal_{timestamp_str}.csv",
            mime="text/csv",
            type="primary",
        )
        st.dataframe(df_skenario_hasil, width="stretch", height=380)

    with tab_d4:
        st.write("Unduh Dokumen Laporan Lengkap dalam format Microsoft Word (.docx):")
        docx_path = "LAPORAN_PROYEK.docx" if os.path.exists("LAPORAN_PROYEK.docx") else "LAPORAN PROYEK.docx"
        
        col_dw1, col_dw2 = st.columns([2, 3])
        with col_dw1:
            if os.path.exists(docx_path):
                with open(docx_path, "rb") as f_docx:
                    st.download_button(
                        label="⬇️ Unduh LAPORAN_PROYEK.docx (Word)",
                        data=f_docx.read(),
                        file_name="LAPORAN_PROYEK.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary",
                    )
                st.success("Berkas Microsoft Word siap diunduh dan diedit langsung.")
            else:
                st.info("Berkas LAPORAN_PROYEK.docx belum digenerate.")
        
        with col_dw2:
            if st.button("🔄 Generate Ulang Berkas Word (.docx)", help="Membuat ulang dokumen LAPORAN_PROYEK.docx"):
                with st.spinner("Memproses pembuatan naskah Word lengkap Bab I - V..."):
                    try:
                        from generate_capstone_word_report import create_capstone_report
                        create_capstone_report("LAPORAN_PROYEK.docx")
                        st.success("Dokumen Word berhasil dibuat ulang!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menghasilkan dokumen: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 1.05rem; padding: 16px 0;">
    Simulasi Persediaan Stok Toko Buku Cardinal &copy; 2026 &bull; Tugas Mata Kuliah Teknik Simulasi dan Pemodelan<br>
    Dikembangkan dengan Python, Streamlit, NumPy, Pandas, dan Plotly.
</div>
""", unsafe_allow_html=True)
