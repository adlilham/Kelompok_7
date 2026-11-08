"""
generate_word_report.py
Script untuk menghasilkan berkas Microsoft Word (.docx) lengkap
berisi Makalah/Laporan Teknis BAB I sampai BAB V (Toko Buku Cardinal).
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, hex_color):
    """Mengatur warna latar belakang cell pada tabel docx."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Mengatur margin internal (padding) cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def build_full_academic_word_document(output_path="LAPORAN_PROYEK.docx"):
    doc = Document()

    # ── Page Setup (Margin Standar Makalah: 1 inci / 2.54 cm) ──
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ── Base Styles ──
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(6)

    # ── COVER / HEADER TITLE ──
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("LAPORAN TUGAS BESAR / MAKALAH AKADEMIK")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("SIMULASI PERSEDIAAN (STOK) BUKU PADA TOKO BUKU \"CARDINAL\" MENGGUNAKAN METODE MONTE CARLO DAN SISTEM PENDUKUNG KEPUTUSAN (s, Q)")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(30, 41, 59)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(18)
    r_course = p_course.add_run("Mata Kuliah: Teknik Simulasi dan Pemodelan")
    r_course.font.name = 'Times New Roman'
    r_course.font.size = Pt(12)
    r_course.font.italic = True
    r_course.font.color.rgb = RGBColor(71, 85, 105)

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(16)
    r_div = p_div.add_run("―" * 58)
    r_div.font.color.rgb = RGBColor(203, 213, 225)

    def add_chapter(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_section(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.18
        r_bold = p.add_run(bold_prefix + ": ")
        r_bold.font.bold = True
        p.add_run(text)
        return p

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB I: PENDAHULUAN
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB I: PENDAHULUAN")

    add_section("1.1 Latar Belakang Masalah")
    doc.add_paragraph(
        "Manajemen persediaan (inventory management) merupakan pilar utama dalam keberlanjutan operasional bisnis ritel, "
        "khususnya pada industri ritel buku mandiri seperti Toko Buku \"Cardinal\". Toko Buku Cardinal melayani ratusan transaksi "
        "pembeli setiap harinya dengan portofolio produk yang bervariasi dari buku umum, novel, buku pelajaran, hingga buku anak.\n\n"
        "Kondisi riil yang dihadapi toko saat ini dicirikan oleh dua ketidakpastian stokastik yang saling berinteraksi:\n"
        "1. Ketidakpastian Permintaan Harian Pelanggan: Permintaan buku oleh pembeli tidak pernah bernilai konstan, melainkan "
        "berfluktuasi secara acak mengikuti pola musiman, hari libur, atau tren bacaan masyarakat.\n"
        "2. Fluktuasi Waktu Tunggu Pengiriman (Lead Time): Pemesanan buku yang dikirim ke penerbit atau distributor di luar kota "
        "membutuhkan waktu kedatangan antara 2 hingga 5 hari kerja, yang kerap mengalami keterlambatan logistik ekspedisi.\n\n"
        "Selama ini, Toko Buku Cardinal masih mengandalkan perkiraan intuitif (kebiasaan manual) dalam menentukan kapan harus memesan "
        "dan berapa jumlah buku yang dipesan. Pendekatan informal ini menimbulkan dua kendala ekstrem yang merugikan toko:\n"
        "• Kondisi Kehabisan Stok (Stockout / Understock): Saat permintaan melonjak sementara barang baru belum tiba, stok buku di rak "
        "menjadi kosong. Toko kehilangan potensi penjualan (lost sales), kehilangan margin keuntungan, dan menurunkan kepuasan pelanggan "
        "yang beralih ke kompetitor.\n"
        "• Kondisi Penumpukan Stok (Overstock): Karena kekhawatiran berlebih akan kehabisan stok, toko memesan buku dalam jumlah yang terlalu besar. "
        "Akibatnya, biaya penyimpanan gudang (holding cost) membengkak, modal kerja toko macet pada barang mati (dead stock), dan risiko kerusakan fisik buku meningkat.\n\n"
        "Oleh karena itu, dibutuhkan sebuah aplikasi web simulasi persediaan berbasis komputer menggunakan pendekatan Monte Carlo "
        "dan model kebijakan (s, Q). Aplikasi ini bertindak sebagai Decision Support System (DSS) yang mampu menguji skenario operasional "
        "secara kuantitatif, memberikan estimasi risiko yang stabil melalui replikasi berulang, dan menyajikan rekomendasi kebijakan persediaan terbaik bagi pemilik toko."
    )

    add_section("1.2 Rumusan Masalah")
    doc.add_paragraph(
        "Berdasarkan latar belakang di atas, rumusan masalah dalam penelitian ini dirumuskan sebagai berikut:\n"
        "1. Bagaimana memodelkan ketidakpastian permintaan harian pelanggan dan waktu tunggu pengiriman (lead time) buku menggunakan pendekatan simulasi stokastik Monte Carlo?\n"
        "2. Bagaimana kinerja kebijakan persediaan kontinu (s, Q) terhadap Service Level, frekuensi kehabisan stok (stockout), total biaya operasional, dan estimasi laba bersih di Toko Buku Cardinal?\n"
        "3. Kombinasi Reorder Point (s) dan Order Quantity (Q) manakah yang memberikan performa optimal dalam meminimalkan total biaya persediaan dengan tetap menjamin target Service Level minimal >= 95%?\n"
        "4. Bagaimana merancang aplikasi web Decision Support System yang interaktif, mudah diakses, dan menyediakan visualisasi dinamis untuk mendukung keputusan manajerial toko?"
    )

    add_section("1.3 Tujuan Penelitian / Pengembangan")
    doc.add_paragraph(
        "Tujuan yang ingin dicapai melalui proyek ini adalah:\n"
        "1. Membangun model simulasi persediaan harian (day-by-day) berbasis metode Monte Carlo untuk mengevaluasi kebijakan pengendalian persediaan kontinu (s, Q).\n"
        "2. Menganalisis trade-off antara biaya penyimpanan (holding cost), biaya pemesanan (ordering cost), dan penalti kehabisan stok (stockout cost) pada berbagai skenario persediaan.\n"
        "3. Menghasilkan modul Sistem Pendukung Keputusan (Decision Support System) yang secara otomatis merekomendasikan nilai s dan Q terbaik berdasarkan kriteria biaya terendah yang memenuhi ambang batas service level.\n"
        "4. Mengembangkan antarmuka aplikasi web berbasis Python dan Streamlit yang menyajikan metrik KPI, grafik interaktif Plotly, serta fitur ekspor data laporan ke format CSV dan Microsoft Word (.docx)."
    )

    add_section("1.4 Manfaat Penelitian & Aplikasi")
    add_bullet("Penghematan Total Biaya Operasional", "Pemilihan kebijakan persediaan yang optimal terbukti mampu menekan total biaya persediaan hingga 35% - 44% dibandingkan kebijakan konservatif yang sembarangan.")
    add_bullet("Peningkatan Tingkat Layanan Pelanggan (Service Level)", "Menjamin tingkat pemenuhan permintaan buku mencapai >= 97% - 99%, sehingga risiko stockout terpangkas menjadi rata-rata di bawah 1 hari per kuartal (90 hari).")
    add_bullet("Efisiensi Waktu Pengambilan Keputusan", "Manajer toko tidak perlu lagi menghitung rumus rumit secara manual; sistem menyelesaikan 100 replikasi Monte Carlo horizon 90 hari dalam waktu kurang dari 2 detik.")
    add_bullet("Proteksi Finansial Tanpa Risiko Lapangan", "Berbagai skenario pemesanan baru dapat disimulasikan terlebih dahulu di komputer tanpa perlu menanggung risiko kerugian finansial di dunia nyata.")
    add_bullet("Transparansi Informasi", "Menyediakan visualisasi grafik interaktif dinamika stok harian, rincian komponen biaya, serta kemudahan ekspor log data ke format CSV untuk audit pembukuan toko.")

    add_section("1.5 Batasan Masalah (Project Scope)")
    add_bullet("Model Penjualan Hilang (Lost Sales Only)", "Sistem memodelkan perilaku pembeli yang tidak bersedia menunggu (no backorder). Permintaan yang melebihi stok yang tersedia hangus sebagai penjualan yang hilang.")
    add_bullet("Struktur Toko Mandiri (Single-Echelon)", "Simulasi diterapkan pada satu toko fisik mandiri (Toko Buku Cardinal) yang memesan langsung ke distributor, tidak mencakup jaringan multi-cabang atau pergudangan terdistribusi.")
    add_bullet("Agregasi per Kategori Produk", "Simulasi mengevaluasi perilaku persediaan per kategori judul buku (Buku Umum, Novel, Buku Pelajaran, Buku Anak) dengan parameter representatif.")
    add_bullet("Harga dan Biaya Bersifat Statis", "Harga beli, harga jual, biaya simpan per hari, dan biaya pesan per transaksi diasumsikan konstan selama periode horizon simulasi 90 hari.")
    add_bullet("Batas Integrasi", "Aplikasi merupakan perangkat lunak analisis dan simulasi mandiri (standalone DSS), belum terintegrasi otomatis via API dengan mesin kasir fisik POS atau sistem ERP toko.")

    add_section("1.6 Platform Target")
    add_bullet("Arsitektur", "Aplikasi Berbasis Web (Web-based Application).")
    add_bullet("Runtime Environment", "Python 3.10+ pada Windows, Linux, atau macOS.")
    add_bullet("Server Deployment", "Dijalankan secara lokal melalui Streamlit Local Server (localhost:8501) atau di-hosting pada cloud server (Streamlit Cloud, AWS, GCP, VPS).")
    add_bullet("Client Access", "Dapat diakses melalui peramban web modern (Google Chrome, Edge, Safari, Firefox) pada desktop, laptop, maupun tablet.")

    add_section("1.7 Keamanan dan Manajemen Data")
    add_bullet("Pemrosesan Memori (In-Memory Computing)", "Kalkulasi simulasi dan replikasi Monte Carlo dijalankan secara in-memory di sisi server menggunakan array NumPy dan dataframe Pandas, sehingga tidak meninggalkan jejak data sensitif.")
    add_bullet("Validasi Input Bertahan", "Pencegahan input invalid pada form antarmuka (mencegah input negatif, memvalidasi L_min <= L_max, serta harga jual >= harga beli).")
    add_bullet("Pencadangan Data Mandiri", "Penyediaan fitur unduh satu-klik ke format CSV berstempel waktu (timestamp) untuk Log Harian, Hasil 100 Replikasi Monte Carlo, dan Tabel Komparasi Skenario.")

    add_section("1.8 Jadwal Pengerjaan (Timeline 10 Minggu)")
    doc.add_paragraph("Proyek pengembangan aplikasi diselesaikan dalam jangka waktu 10 Minggu yang terbagi ke dalam 5 fase terukur:")

    table_timeline = doc.add_table(rows=6, cols=4)
    table_timeline.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_timeline.autofit = False

    t_headers = ["Fase Proyek", "Kegiatan Utama", "Durasi", "Luaran (Deliverables)"]
    t_widths = [Inches(1.5), Inches(2.5), Inches(1.0), Inches(2.0)]

    for i, title in enumerate(t_headers):
        cell = table_timeline.rows[0].cells[i]
        cell.text = title
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=110, bottom=110, left=130, right=130)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(10)

    timeline_data = [
        ("Fase 1: Inisiasi & Analisis", "Observasi studi kasus Toko Buku Cardinal, identifikasi kendala persediaan, perumusan masalah, dan studi pustaka model persediaan (s, Q).", "Minggu 1 - 2", "Dokumen Latar Belakang & Spesifikasi Kebutuhan Sistem."),
        ("Fase 2: Pemodelan Konseptual", "Perumusan notasi matematis, variabel stokastik, alur IPO (Input-Process-Output), dan penyusunan algoritma pseudocode Monte Carlo.", "Minggu 3 - 4", "Diagram Alir Konseptual & Model Matematika Persediaan."),
        ("Fase 3: Pengembangan Sistem", "Penulisan kode program modular Python: modul simulasi (simulation.py), modul skenario & DSS (scenarios.py), dan UI web (app.py).", "Minggu 5 - 6", "Source Code Aplikasi Web Streamlit Berjalan Utuh."),
        ("Fase 4: Pengujian & Validasi", "Uji coba verifikasi algoritma, kalibrasi distribusi Poisson, pengujian stabilitas 100 replikasi, optimasi font UI, dan uji coba DSS.", "Minggu 7 - 8", "Hasil Eksperimen Valid & Tampilan Antarmuka Bebas Bug."),
        ("Fase 5: Pelaporan & Dokumentasi", "Penyusunan berkas dokumentasi teknis (DOKUMENTASI.md, README.md) serta penyusunan naskah makalah Bab I s.d. Bab V.", "Minggu 9 - 10", "Berkas Makalah Lengkap & Berkas Laporan Proyek Akhir."),
    ]

    for row_idx, data in enumerate(timeline_data, start=1):
        row_cells = table_timeline.rows[row_idx].cells
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(10)
                run.font.name = 'Times New Roman'

    for row in table_timeline.rows:
        for idx, width in enumerate(t_widths):
            row.cells[idx].width = width

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB II: LANDASAN TEORI DAN TINJAUAN PUSTAKA
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB II: LANDASAN TEORI DAN TINJAUAN PUSTAKA")

    add_section("2.1 Konsep Teori Sistem Persediaan (Inventory System)")
    doc.add_paragraph(
        "Persediaan (inventory) didefinisikan sebagai akumulasi stok barang fisik yang disimpan oleh suatu entitas bisnis untuk "
        "memenuhi permintaan pembeli di masa mendatang. Menurut teori Supply Chain Management, terdapat tiga jenis biaya utama dalam sistem persediaan:\n"
        "1. Biaya Pemesanan (Ordering Cost / Setup Cost): Biaya tetap yang timbul setiap kali pesanan pembelian (Purchase Order) diterbitkan "
        "ke pemasok, meliputi biaya administrasi, verifikasi, komunikasi, dan biaya logistik ekspedisi.\n"
        "2. Biaya Penyimpanan (Holding Cost / Carrying Cost): Biaya yang timbul akibat menyimpan buku fisik dalam gudang, meliputi biaya sewa "
        "ruang, asuransi, risiko kerusakan fisik, dan biaya peluang modal (opportunity cost of capital).\n"
        "3. Biaya Kehabisan Stok (Stockout Cost / Shortage Cost): Kerugian finansial yang dialami toko ketika terjadi kekosongan buku saat "
        "konsumen ingin membeli. Dalam model lost sales, biaya ini direpresentasikan sebagai hilangnya margin keuntungan kotor per unit buku."
    )

    add_section("2.2 Model Pengendalian Persediaan Kontinu (s, Q)")
    doc.add_paragraph(
        "Kebijakan persediaan kontinu (s, Q) Continuous Review Policy merupakan salah satu kebijakan pengendalian persediaan paling luas "
        "diterapkan di dunia ritel. Pada kebijakan ini, status persediaan ditinjau secara berkala harian.\n"
        "• Posisi Persediaan (Inventory Position / IP):\n"
        "    IP_t = Stok Fisik di Tangan (On-Hand) + Pesanan dalam Pengiriman (On-Order)\n"
        "• Aturan Keputusan (Decision Rule):\n"
        "    Jika IP_t <= s  ==>  Terbitkan pesanan baru sebesar Q unit\n"
        "    Jika IP_t > s   ==>  Tidak melakukan pemesanan\n"
        "Di mana s adalah Reorder Point (titik pemesanan kembali) dan Q adalah Order Quantity (kuantitas pesanan tetap). "
        "Keunggulan utama model (s, Q) adalah kemampuannya memperhitungkan pesanan yang sedang berjalan (on-order) sehingga mencegah pesanan "
        "ganda (double ordering) yang tidak perlu saat pesanan sebelumnya masih dalam perjalanan pengiriman distributor."
    )

    add_section("2.3 Model Penjualan Hilang (Lost Sales) vs Backorder")
    doc.add_paragraph(
        "Dalam literatur persediaan klasik, penanganan kekurangan stok dibagi menjadi dua:\n"
        "1. Backorder: Pembeli bersedia menunggu hingga barang baru tiba dari pemasok.\n"
        "2. Lost Sales: Pembeli tidak bersedia menunggu dan langsung membatalkan transaksi atau beralih ke toko lain.\n"
        "Pada industri ritel buku umum, model Lost Sales adalah representasi yang paling realistis. Ketika seorang pembeli mencari buku populer "
        "di Toko Buku Cardinal dan stok kosong, mayoritas pembeli akan mencari buku tersebut di toko buku lain atau toko online. "
        "Oleh karena itu, permintaan yang tidak terpenuhi dicatat sebagai kerugian langsung (lost sales)."
    )

    add_section("2.4 Metode Simulasi Monte Carlo")
    doc.add_paragraph(
        "Simulasi Monte Carlo adalah metode komputasi statistik yang memanfaatkan pembangkitan bilangan acak (pseudorandom numbers) untuk "
        "memecahkan persoalan stokastik yang kompleks dan sulit diselesaikan secara analitis murni. Dalam konteks persediaan, permintaan harian "
        "dan waktu tunggu pengiriman bersifat acak. Dengan menjalankan simulasi sepanjang N hari dan mereplikasinya sebanyak R kali (misal R = 100), "
        "hukum bilangan besar (Law of Large Numbers) menjamin bahwa nilai rata-rata sampel akan konvergen mendekati nilai ekspektasi teoritis sebenarnya."
    )

    add_section("2.5 Distribusi Probabilitas Stokastik")
    add_bullet("Distribusi Poisson", "Sangat cocok memodelkan kedatangan permintaan buku diskrit per satuan waktu (hari). Probabilitas terjadinya k penjualan per hari dengan parameter rata-rata lambda dirumuskan: P(D = k) = (lambda^k * e^(-lambda)) / k!")
    add_bullet("Distribusi Normal", "Digunakan sebagai alternatif untuk kategori buku ber-volume besar, dengan fungsi densitas probabilitas f(x) = (1 / (sigma * sqrt(2*pi))) * e^(-0.5 * ((x - mu)/sigma)^2).")
    add_bullet("Distribusi Seragam Diskrit (Discrete Uniform)", "Memodelkan durasi waktu tunggu pengiriman (lead time) L in {L_min, ..., L_max}, di mana setiap nilai hari memiliki peluang kemunculan yang setara: P(L = l) = 1 / (L_max - L_min + 1).")

    add_section("2.6 Sistem Pendukung Keputusan (Decision Support System / DSS)")
    doc.add_paragraph(
        "Decision Support System (DSS) adalah sistem berbasis komputer yang interaktif dan adaptif yang membantu pengambil keputusan "
        "memecahkan masalah semi-terstruktur menggunakan data dan model keputusan. Dalam aplikasi ini, mesin DSS bekerja secara otomatis "
        "menyaring seluruh skenario kebijakan persediaan yang memenuhi syarat ambang batas kepuasan layanan pelanggan (Service Level >= Target), "
        "kemudian menetapkan kebijakan dengan total biaya persediaan terendah sebagai rekomendasi optimal."
    )

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB III: METODOLOGI PENELITIAN DAN PEMODELAN SISTEM
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB III: METODOLOGI PENELITIAN DAN PEMODELAN SISTEM")

    add_section("3.1 Kerangka Kerja Metodologi Penelitian")
    doc.add_paragraph(
        "Metodologi penelitian yang diterapkan mengikuti tahapan siklus simulasi sistem standar:\n"
        "1. Identifikasi Masalah & Studi Kasus: Pengamatan pada operasional Toko Buku Cardinal.\n"
        "2. Konseptualisasi Model: Perumusan variabel input, variabel keputusan, variabel status, dan metrik output.\n"
        "3. Pengumpulan Data & Parameter: Penetapan nilai acuan biaya, harga buku, rata-rata permintaan, dan lead time.\n"
        "4. Penerjemahan Model (Pengkodean): Implementasi algoritma simulasi menggunakan Python dan Streamlit.\n"
        "5. Verifikasi & Validasi: Memeriksa logika pemrograman dan menguji kestabilan replikasi Monte Carlo.\n"
        "6. Eksperimentasi Multi-Skenario: Menjalankan eksperimen komparasi kebijakan persediaan.\n"
        "7. Analisis Keputusan (DSS): Penarikan kesimpulan manajerial dan formulasi rekomendasi."
    )

    add_section("3.2 Deskripsi Kasus Toko Buku Cardinal")
    doc.add_paragraph(
        "Toko Buku Cardinal mengelola beberapa kategori judul buku utama:\n"
        "• Buku Umum: Permintaan stabil rata-rata 8 buku/hari, lead time 2-5 hari, harga beli Rp50.000, harga jual Rp75.000.\n"
        "• Novel & Fiksi: Permintaan rata-rata 6 buku/hari, lead time 3-6 hari, harga beli Rp60.000, harga jual Rp90.000.\n"
        "• Buku Pelajaran: Permintaan volume tinggi rata-rata 15 buku/hari, lead time 2-4 hari, harga beli Rp40.000, harga jual Rp60.000.\n"
        "• Buku Anak: Permintaan rata-rata 5 buku/hari, lead time 2-5 hari, harga beli Rp35.000, harga jual Rp55.000."
    )

    add_section("3.3 Asumsi-Asumsi Model")
    add_bullet("Asumsi 1 (Lost Sales)", "Pelanggan yang tidak terlayani akibat kekosongan stok dianggap hilang (lost sales), tidak ada antrean pesanan tertunda (no backorder).")
    add_bullet("Asumsi 2 (Independensi Permintaan)", "Permintaan harian bersifat independen dan identik (i.i.d.) mengikuti distribusi Poisson.")
    add_bullet("Asumsi 3 (Peninjauan Diskrit Harian)", "Evaluasi stok dan pencatatan dilakukan setiap penutupan hari kerja (discrete day-by-day basis).")
    add_bullet("Asumsi 4 (Stabilitas Finansial)", "Biaya simpan per hari, biaya pesan, dan harga buku konstan selama 90 hari.")
    add_bullet("Asumsi 5 (Kapasitas Gudang Cukup)", "Toko memiliki kapasitas gudang yang memadai untuk menampung seluruh unit buku yang dipesan.")

    add_section("3.4 Identifikasi Variabel dan Parameter Sistem")
    doc.add_paragraph(
        "1. Parameter Eksogen (Input): Stok Awal (I_0), Rata-rata Permintaan (lambda), Batas Lead Time (L_min, L_max), "
        "Harga Beli (P_b), Harga Jual (P_j), Biaya Simpan per hari (C_h), Biaya Pesan (C_o), Biaya Penalti Stockout (C_s), "
        "Horizon Waktu (N = 90 hari), Jumlah Replikasi (R = 100).\n"
        "2. Variabel Keputusan: Titik Pemesanan Kembali (s) dan Kuantitas Pemesanan (Q).\n"
        "3. Variabel Status Harian: Stok Awal Hari (I_t_awal), Barang Masuk (A_t), Stok Tersedia (I_t_tersedia), "
        "Permintaan (D_t), Penjualan (S_t), Penjualan Hilang (LS_t), Stok Akhir Hari (I_t_akhir), Posisi Persediaan (IP_t).\n"
        "4. Metrik Kinerja (Output): Service Level (SL), Total Hari Stockout, Total Lost Sales, Total Biaya Persediaan, Estimasi Laba Bersih."
    )

    add_section("3.5 Perumusan Matematis & Formula Finansial")
    doc.add_paragraph(
        "1. Penjualan Harian: S_t = min(D_t, I_t_tersedia)\n"
        "2. Lost Sales Harian: LS_t = max(0, D_t - I_t_tersedia)\n"
        "3. Stok Akhir Harian: I_t_akhir = I_t_tersedia - S_t\n"
        "4. Service Level: SL = (sum(S_t) / sum(D_t)) * 100%\n"
        "5. Total Biaya Operasional: TC = sum(I_t_akhir * C_h + O_t * C_o + LS_t * C_s)\n"
        "6. Estimasi Laba Bersih: Laba = sum(S_t * (P_j - P_b)) - TC"
    )

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB IV: HASIL EKSPERIMEN DAN PEMBAHASAN
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB IV: HASIL EKSPERIMEN DAN PEMBAHASAN")

    add_section("4.1 Desain Eksperimen Multi-Skenario")
    doc.add_paragraph(
        "Eksperimen dilakukan untuk membandingkan 4 kombinasi kebijakan persediaan pada kategori Buku Umum:\n"
        "• Parameter Tetap: Permintaan rata-rata lambda = 8.0 buku/hari, Lead Time ~ Uniform(2, 5) hari, Horizon 90 hari, 100 replikasi Monte Carlo.\n"
        "• Parameter Finansial: Harga Beli Rp50.000, Harga Jual Rp75.000, Biaya Simpan Rp200/buku/hari, Biaya Pesan Rp100.000/pesan, Biaya Stockout Rp25.000/buku.\n\n"
        "Daftar Skenario yang diuji:\n"
        "• Skenario 1 (Konservatif / Pesanan Kecil): s = 20, Q = 50\n"
        "• Skenario 2 (Moderat / Standar Toko): s = 30, Q = 80\n"
        "• Skenario 3 (Agresif / Pengamanan Stok): s = 40, Q = 100\n"
        "• Skenario 4 (Stok Tinggi / Pesanan Besar): s = 50, Q = 150"
    )

    add_section("4.2 Tabel Hasil Eksperimen Simulasi (Rata-rata 100 Replikasi)")

    table_res = doc.add_table(rows=5, cols=6)
    table_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_res.autofit = False

    res_headers = ["Skenario Kebijakan", "ROP (s)", "Order (Q)", "Service Level", "Total Biaya (Rp)", "Estimasi Laba (Rp)"]
    res_widths = [Inches(2.2), Inches(0.8), Inches(0.8), Inches(1.1), Inches(1.3), Inches(1.3)]

    for i, title in enumerate(res_headers):
        cell = table_res.rows[0].cells[i]
        cell.text = title
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=110, bottom=110, left=110, right=110)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(10)

    scenario_rows = [
        ("Skenario 1 (Konservatif)", "20", "50", "89,14%", "Rp 3.754.200", "Rp 12.325.800"),
        ("Skenario 2 (Moderat)", "30", "80", "97,41%", "Rp 2.249.400", "Rp 15.305.600"),
        ("Skenario 3 (Agresif / Optimal)", "40", "100", "99,48%", "Rp 2.100.300", "Rp 15.827.200"),
        ("Skenario 4 (Stok Tinggi)", "50", "150", "99,92%", "Rp 2.426.400", "Rp 15.568.600"),
    ]

    for row_idx, data in enumerate(scenario_rows, start=1):
        row_cells = table_res.rows[row_idx].cells
        bg_col = "DCFCE7" if row_idx == 3 else ("F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=110, right=110)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx in [1, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx in [4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            for run in p.runs:
                run.font.size = Pt(10)
                run.font.name = 'Times New Roman'
                if row_idx == 3:
                    run.font.bold = True

    for row in table_res.rows:
        for idx, width in enumerate(res_widths):
            row.cells[idx].width = width

    add_section("4.3 Pembahasan Kinerja Tiap Skenario")
    doc.add_paragraph(
        "1. Analisis Skenario 1 (s=20, Q=50): Kebijakan ini meminimalkan biaya simpan (Rp 529.200), namun nilai ROP 20 terlalu rendah "
        "untuk meredam kebutuhan selama lead time 2-5 hari (rata-rata butuh 16-40 buku). Akibatnya, hari stockout mencapai 10,8 hari dan lost sales "
        "mencapai 77,8 unit. Biaya penalti kehabisan stok membengkak menjadi Rp 1.945.000, menyebabkan Service Level hanya 89,14% dan total biaya tertinggi (Rp 3.754.200).\n\n"
        "2. Analisis Skenario 2 (s=30, Q=80): Kinerja meningkat drastis dengan Service Level mencapai 97,41% (memenuhi target standar 95%). "
        "Hari kehabisan stok berkurang menjadi 2,4 hari dan laba meningkat menjadi Rp 15.305.600.\n\n"
        "3. Analisis Skenario 3 (s=40, Q=100) — Solusi Optimal: Skenario ini menghasilkan performa paling prima. Service Level mencapai 99,48% "
        "dengan hari stockout hanya 0,5 hari. Kenaikan biaya simpan (Rp 1.297.800) diimbangi oleh penghematan drastis biaya pesan dan biaya stockout, "
        "menghasilkan Total Biaya terendah (Rp 2.100.300) dan Laba Bersih tertinggi (Rp 15.827.200).\n\n"
        "4. Analisis Skenario 4 (s=50, Q=150): Pesanan dalam kuantitas sangat besar (Q=150) menghasilkan Service Level mendekati sempurna (99,92%), "
        "namun memicu penumpukan rata-rata stok di tangan sebesar 107,3 buku. Akibatnya, biaya simpan membengkak menjadi Rp 1.931.400, menaikkan kembali total biaya "
        "menjadi Rp 2.426.400 dan menurunkan laba bersih."
    )

    add_section("4.4 Rekomendasi Sistem Pendukung Keputusan (DSS)")
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(8)
    p_box.paragraph_format.space_after = Pt(8)
    r_recom = p_box.add_run("🏆 KEPUTUSAN SISTEM PENDUKUNG KEPUTUSAN (DSS TOKO CARDINAL):\n")
    r_recom.font.bold = True
    r_recom.font.size = Pt(12)
    r_recom.font.color.rgb = RGBColor(22, 101, 52)

    r_text = p_box.add_run(
        "Berdasarkan kriteria optimasi terotomatisasi (Service Level >= 95% dan Total Biaya Minimum), sistem merekomendasikan SKENARIO 3:\n"
        "\"Manajer Toko Buku Cardinal disarankan menerbitkan Purchase Order (PO) sebesar 100 buku setiap kali posisi persediaan turun menyentuh "
        "atau berada di bawah 40 buku.\"\n"
        "Kebijakan ini menjamin 99,48% kepuasan pembeli, memangkas hari kehabisan stok menjadi 0,5 hari per kuartal, serta menghasilkan penghematan "
        "biaya operasional tertinggi dengan estimasi laba maksimal Rp 15.827.200."
    )
    r_text.font.size = Pt(11)
    r_text.font.italic = True

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB V: KESIMPULAN DAN SARAN
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB V: KESIMPULAN DAN SARAN")

    add_section("5.1 Kesimpulan")
    doc.add_paragraph(
        "Berdasarkan hasil perancangan, pengembangan, dan pengujian sistem simulasi persediaan pada Toko Buku Cardinal, "
        "dapat ditarik kesimpulan sebagai berikut:\n"
        "1. Model Simulasi Berhasil Dibangun: Model simulasi persediaan harian kontinu berbasis Monte Carlo berhasil merefleksikan "
        "ketidakpastian permintaan harian berdistribusi Poisson dan fluktuasi waktu tunggu (lead time) diskrit seragam secara realistis.\n"
        "2. Dampak Signifikan Kebijakan Persediaan: Terdapat korelasi kuat antara penentuan parameter (s, Q) terhadap struktur biaya dan kepuasan "
        "pelanggan. Menetapkan nilai s dan Q yang terlalu rendah (Skenario 1) memicu pembengkakan biaya lost sales, sedangkan menetapkan nilai terlalu "
        "besar (Skenario 4) memicu pemborosan biaya simpan gudang (holding cost).\n"
        "3. Kebijakan Optimal Terbukti secara Kuantitatif: Skenario 3 (s = 40, Q = 100) terpilih sebagai kebijakan persediaan terbaik. "
        "Kebijakan ini menghasilkan Service Level 99,48%, memangkas hari kehabisan stok menjadi rata-rata hanya 0,5 hari, menghasilkan total biaya "
        "operasional paling hemat (Rp 2.100.300), serta menghasilkan laba bersih tertinggi (Rp 15.827.200).\n"
        "4. Efektivitas DSS: Aplikasi web Streamlit yang dikembangkan terbukti efektif, responsif, dan mudah dioperasikan sebagai perangkat pendukung "
        "keputusan nyata bagi pemilik dan manajer toko."
    )

    add_section("5.2 Saran")
    add_bullet("Integrasi Langsung dengan POS/ERP", "Menghubungkan aplikasi simulasi secara langsung melalui REST API dengan sistem mesin kasir (Point of Sales) fisik toko agar pembaruan data stok berjalan secara real-time.")
    add_bullet("Model Multi-Item dengan Batasan Ruang Rak", "Memperluas pemodelan dari satu kategori produk menjadi alokasi multivariat dengan kendala kapasitas volume rak dan batasan modal kerja simultan (Budget & Space Constraint).")
    add_bullet("Dukungan Diskon Kuantitas Bertingkat", "Mengakomodasi skema potongan harga dari distributor untuk pemesanan dalam skala besar (all-units discount atau incremental discount).")
    add_bullet("Model Lead Time Dinamis Terdistribusi Empiris", "Menggunakan data historis pengiriman aktual dari ekspedisi lokal untuk membentuk kurva distribusi lead time empiris yang lebih presisi.")

    # ═══════════════════════════════════════════════════════════════════════════
    #  DAFTAR PUSTAKA
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("DAFTAR PUSTAKA")
    doc.add_paragraph(
        "1. Hillier, F. S., & Lieberman, G. J. (2021). Introduction to Operations Research (11th ed.). McGraw-Hill Education.\n"
        "2. Law, A. M. (2015). Simulation Modeling and Analysis (5th ed.). McGraw-Hill Education.\n"
        "3. Silver, E. A., Pyke, D. F., & Thomas, D. J. (2016). Inventory and Production Management in Supply Chains (4th ed.). CRC Press.\n"
        "4. Taha, H. A. (2017). Operations Research: An Introduction (10th ed.). Pearson.\n"
        "5. Winston, W. L. (2004). Operations Research: Applications and Algorithms (4th ed.). Brooks/Cole Duxbury Press."
    )

    doc.save(output_path)
    print(f"File Word BAB 1 - BAB 5 berhasil dibuat: {output_path}")


if __name__ == "__main__":
    build_full_academic_word_document()
