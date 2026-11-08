"""
scenarios.py - Modul Eksperimen Skenario dan Sistem Pendukung Keputusan (DSS)
Mata Kuliah: Teknik Simulasi dan Pemodelan

Modul ini mengelola evaluasi berbagai kombinasi kebijakan persediaan (s, Q),
membandingkan performa biaya & service level, serta menghasilkan rekomendasi
kebijakan terbaik untuk pengambil keputusan di Toko Buku Cardinal.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
from simulation import SimulationConfig, jalankan_monte_carlo


def dapatkan_skenario_default() -> List[Dict[str, Any]]:
    """Mengembalikan daftar 4 skenario standar persediaan (s, Q)."""
    return [
        {
            "id": 1,
            "nama": "Skenario 1 (Konservatif / Pesanan Kecil)",
            "rop": 20,
            "q": 50,
            "deskripsi": "ROP rendah & pesanan kecil, meminimalkan biaya simpan namun rentan stockout.",
        },
        {
            "id": 2,
            "nama": "Skenario 2 (Moderat / Standar Toko)",
            "rop": 30,
            "q": 80,
            "deskripsi": "Kebijakan seimbang antara frekuensi pemesanan dan ketersediaan stok buku.",
        },
        {
            "id": 3,
            "nama": "Skenario 3 (Agresif / Pengamanan Stok)",
            "rop": 40,
            "q": 100,
            "deskripsi": "ROP lebih tinggi untuk meredam lonjakan permintaan dan fluktuasi lead time.",
        },
        {
            "id": 4,
            "nama": "Skenario 4 (Stok Tinggi / Pesanan Besar)",
            "rop": 50,
            "q": 150,
            "deskripsi": "Volume pesanan besar untuk meminimalkan biaya pemesanan berulang, persediaan melimpah.",
        },
    ]


def jalankan_analisis_skenario(
    daftar_skenario: List[Dict[str, Any]],
    base_config: SimulationConfig
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Menjalankan simulasi Monte Carlo untuk setiap skenario dalam daftar.
    
    Returns:
        df_perbandingan: DataFrame rangkuman metrik per skenario
        dict_replikasi: Dict skenario_nama -> DataFrame replikasi (untuk histogram/box plot)
    """
    ringkasan_list = []
    dict_replikasi = {}

    for skenario in daftar_skenario:
        # Clone konfigurasi dasar dan timpa nilai ROP dan Q
        config_skenario = SimulationConfig(
            reorder_point=int(skenario["rop"]),
            order_quantity=int(skenario["q"]),
            safety_stock=base_config.safety_stock,
            stok_awal=base_config.stok_awal,
            distribusi_permintaan=base_config.distribusi_permintaan,
            rata_permintaan=base_config.rata_permintaan,
            std_permintaan=base_config.std_permintaan,
            lead_time_min=base_config.lead_time_min,
            lead_time_max=base_config.lead_time_max,
            lead_time_mode=base_config.lead_time_mode,
            periode_hari=base_config.periode_hari,
            jumlah_replikasi=base_config.jumlah_replikasi,
            random_seed=base_config.random_seed,
            harga_beli=base_config.harga_beli,
            harga_jual=base_config.harga_jual,
            biaya_simpan_per_hari=base_config.biaya_simpan_per_hari,
            biaya_pesan_per_order=base_config.biaya_pesan_per_order,
            biaya_stockout_per_unit=base_config.biaya_stockout_per_unit,
        )

        ringkasan, df_rep, _ = jalankan_monte_carlo(config_skenario)
        nama = skenario["nama"]
        dict_replikasi[nama] = df_rep

        ringkasan_list.append({
            "Skenario": nama,
            "ROP (s)": skenario["rop"],
            "Order Qty (Q)": skenario["q"],
            "Service Level (%)": ringkasan["service_level_mean"],
            "Hari Stockout": ringkasan["hari_stockout_mean"],
            "Lost Sales (Buku)": ringkasan["lost_sales_mean"],
            "Rata-rata Stok": ringkasan["rata_stok_mean"],
            "Frekuensi Pesan": ringkasan["frekuensi_pesanan_mean"],
            "Biaya Simpan (Rp)": ringkasan["biaya_simpan_mean"],
            "Biaya Pesan (Rp)": ringkasan["biaya_pesan_mean"],
            "Biaya Stockout (Rp)": ringkasan["biaya_stockout_mean"],
            "Total Biaya (Rp)": ringkasan["total_biaya_mean"],
            "Estimasi Laba (Rp)": ringkasan["laba_mean"],
            "Deskripsi": skenario.get("deskripsi", ""),
        })

    df_perbandingan = pd.DataFrame(ringkasan_list)
    return df_perbandingan, dict_replikasi


def berikan_rekomendasi_keputusan(
    df_perbandingan: pd.DataFrame,
    target_service_level: float = 95.0
) -> Dict[str, Any]:
    """
    Sistem Pendukung Keputusan (Decision Support System):
    Memilih skenario kebijakan persediaan terbaik dengan kriteria:
    1. Memenuhi batas ambang toleransi Service Level minimal (>= target_service_level).
    2. Dari kumpulan skenario yang lolos, pilih yang memiliki Total Biaya terendah
       (atau Laba tertinggi).
    3. Jika tidak ada skenario yang memenuhi target, berikan peringatan dan pilih skenario
       dengan Service Level tertinggi terdekat beserta rekomendasi penyesuaian.
    """
    if df_perbandingan.empty:
        return {
            "status": "ERROR",
            "pesan": "Tabel perbandingan skenario kosong.",
            "skenario_terpilih": None,
            "evaluasi_semua": [],
        }

    # Evaluasi status setiap skenario
    evaluasi_semua = []
    for _, row in df_perbandingan.iterrows():
        sl = float(row["Service Level (%)"])
        biaya = float(row["Total Biaya (Rp)"])
        laba = float(row["Estimasi Laba (Rp)"])
        lolos = sl >= target_service_level
        evaluasi_semua.append({
            "skenario": row["Skenario"],
            "rop": int(row["ROP (s)"]),
            "q": int(row["Order Qty (Q)"]),
            "service_level": sl,
            "total_biaya": biaya,
            "laba": laba,
            "lolos": lolos,
        })

    # Filter skenario yang lolos kualifikasi target service level
    skenario_lolos = df_perbandingan[df_perbandingan["Service Level (%)"] >= target_service_level]

    if not skenario_lolos.empty:
        # Pilih yang total biayanya minimum di antara yang lolos
        skenario_terpilih = skenario_lolos.sort_values(by="Total Biaya (Rp)", ascending=True).iloc[0]
        
        status = "OPTIMAL"
        kalimat_utama = (
            f"Disarankan memesan {int(skenario_terpilih['Order Qty (Q)'])} buku "
            f"ketika posisi stok mencapai {int(skenario_terpilih['ROP (s)'])} buku."
        )
        
        alasan = [
            f"<b>Service Level Tercapai</b>: Memenuhi target minimal {target_service_level:.1f}% dengan capaian <b>{skenario_terpilih['Service Level (%)']:.2f}%</b>.",
            f"<b>Efisiensi Biaya Terbaik</b>: Menghasilkan total biaya terendah di antara seluruh kandidat yang memenuhi syarat, yaitu <b>Rp {skenario_terpilih['Total Biaya (Rp)']:,.0f}</b>.",
            f"<b>Profitabilitas Maksimal</b>: Memberikan estimasi laba bersih rata-rata sebesar <b>Rp {skenario_terpilih['Estimasi Laba (Rp)']:,.0f}</b>.",
            f"<b>Keseimbangan Risiko</b>: Rata-rata hari stockout hanya <b>{skenario_terpilih['Hari Stockout']:.1f} hari</b> dengan total lost sales <b>{skenario_terpilih['Lost Sales (Buku)']:.1f} buku</b> selama periode horizon.",
        ]

        # Berikan status pada evaluasi
        for item in evaluasi_semua:
            if item["skenario"] == skenario_terpilih["Skenario"]:
                item["status_label"] = "🏆 Terpilih (Optimal)"
                item["catatan"] = "Memenuhi target service level dengan total biaya paling hemat."
            elif item["lolos"]:
                item["status_label"] = "✅ Lolos Kriteria"
                item["catatan"] = f"Service level aman ({item['service_level']:.1f}%), namun biaya lebih tinggi."
            else:
                item["status_label"] = "❌ Tidak Lolos"
                item["catatan"] = f"Service level ({item['service_level']:.1f}%) di bawah target {target_service_level:.1f}%."

        return {
            "status": status,
            "kalimat_utama": kalimat_utama,
            "nama_skenario": skenario_terpilih["Skenario"],
            "rop": int(skenario_terpilih["ROP (s)"]),
            "q": int(skenario_terpilih["Order Qty (Q)"]),
            "service_level": float(skenario_terpilih["Service Level (%)"]),
            "total_biaya": float(skenario_terpilih["Total Biaya (Rp)"]),
            "laba": float(skenario_terpilih["Estimasi Laba (Rp)"]),
            "alasan": alasan,
            "skenario_row": skenario_terpilih.to_dict(),
            "catatan": "Kebijakan ini memberikan kombinasi paling optimal antara kepuasan pembeli dan efisiensi modal kerja.",
            "evaluasi_semua": evaluasi_semua,
        }
    else:
        # Tidak ada yang memenuhi target
        skenario_terbaik = df_perbandingan.sort_values(by="Service Level (%)", ascending=False).iloc[0]
        
        status = "PERINGATAN"
        kalimat_utama = (
            f"⚠️ Peringatan: Tidak ada skenario yang memenuhi target Service Level minimal {target_service_level:.1f}%."
        )
        
        alasan = [
            f"Target kepuasan pembeli ({target_service_level:.1f}%) terlalu ketat dibandingkan kapasitas kebijakan persediaan yang diuji.",
            f"Skenario dengan performa pemenuhan tertinggi saat ini adalah <b>{skenario_terbaik['Skenario']}</b> dengan Service Level <b>{skenario_terbaik['Service Level (%)']:.2f}%</b>.",
            f"Untuk mencapai target {target_service_level:.1f}%, disarankan <b>menaikkan Reorder Point (ROP > {int(skenario_terbaik['ROP (s)'])} buku)</b> atau <b>menambah Order Quantity (Q > {int(skenario_terbaik['Order Qty (Q)'])} buku)</b> guna mengantisipasi keterlambatan lead time.",
        ]

        for item in evaluasi_semua:
            if item["skenario"] == skenario_terbaik["Skenario"]:
                item["status_label"] = "⚠️ Terdekat"
                item["catatan"] = f"Service level tertinggi ({item['service_level']:.1f}%), namun belum tembus target {target_service_level:.1f}%."
            else:
                item["status_label"] = "❌ Tidak Lolos"
                item["catatan"] = f"Service level ({item['service_level']:.1f}%) di bawah target."

        return {
            "status": status,
            "kalimat_utama": kalimat_utama,
            "nama_skenario": skenario_terbaik["Skenario"],
            "rop": int(skenario_terbaik["ROP (s)"]),
            "q": int(skenario_terbaik["Order Qty (Q)"]),
            "service_level": float(skenario_terbaik["Service Level (%)"]),
            "total_biaya": float(skenario_terbaik["Total Biaya (Rp)"]),
            "laba": float(skenario_terbaik["Estimasi Laba (Rp)"]),
            "alasan": alasan,
            "skenario_row": skenario_terbaik.to_dict(),
            "catatan": "Tingkatkan nilai ROP atau evaluasi kembali target service level sesuai batasan modal kerja.",
            "evaluasi_semua": evaluasi_semua,
        }
