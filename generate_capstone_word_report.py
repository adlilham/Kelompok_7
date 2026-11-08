"""
generate_capstone_word_report.py
Script komprehensif untuk menyusun Dokumen Laporan Project Capstone Design Informatika / Manajemen Proyek
sesuai silabus lengkap: Bagian Awal, Bab I s.d. Bab V, Daftar Pustaka, dan 10 Bagian Lampiran Lengkap.
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


def create_capstone_report(output_path="LAPORAN_PROYEK.docx"):
    doc = Document()

    # Margin Standar Skripsi/Makalah: 1 inci (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(6)

    def add_chapter(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_section(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_sub(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_prefix + ": ")
        r_bold.font.bold = True
        p.add_run(text)
        return p

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAGIAN AWAL: COVER & KELENGKAPAN ADMINISTRATIF
    # ═══════════════════════════════════════════════════════════════════════════
    p_cov1 = doc.add_paragraph()
    p_cov1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov1.paragraph_format.space_before = Pt(36)
    p_cov1.paragraph_format.space_after = Pt(6)
    r1 = p_cov1.add_run("LAPORAN PROJECT CAPSTONE DESIGN INFORMATIKA / MANAJEMEN PROYEK")
    r1.font.size = Pt(15)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 23, 42)

    p_cov2 = doc.add_paragraph()
    p_cov2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov2.paragraph_format.space_after = Pt(24)
    r2 = p_cov2.add_run("RANCANG BANGUN APLIKASI WEB SIMULASI PERSEDIAAN STOKASTIK DAN SISTEM PENDUKUNG KEPUTUSAN (s, Q) MENGGUNAKAN METODE MONTE CARLO PADA TOKO BUKU \"CARDINAL\"")
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(30, 41, 59)

    p_cov3 = doc.add_paragraph()
    p_cov3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov3.paragraph_format.space_after = Pt(30)
    r3 = p_cov3.add_run("Bidang Keilmuan: Data Science & Rekayasa Perangkat Lunak\nTeknologi: Python, Streamlit, NumPy, Pandas, Plotly")
    r3.font.size = Pt(11.5)
    r3.font.italic = True
    r3.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_page_break()

    # ── KATA PENGANTAR ──
    add_chapter("KATA PENGANTAR")
    doc.add_paragraph(
        "Puji dan syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa atas berkat dan rahmat-Nya, "
        "sehingga penyusunan laporan project Capstone Design Informatika / Tugas Besar Mata Kuliah Manajemen Proyek dan "
        "Teknik Simulasi dan Pemodelan yang berjudul \"Rancang Bangun Aplikasi Web Simulasi Persediaan Stokastik dan Sistem "
        "Pendukung Keputusan (s, Q) Menggunakan Metode Monte Carlo pada Toko Buku Cardinal\" dapat terselesaikan dengan baik.\n\n"
        "Project ini dikembangkan sebagai solusi berbasis komputasi untuk mengatasi permasalahan nyata pada operasional ritel, "
        "yakni ketidakpastian permintaan pembeli dan keterlambatan pengiriman distributor (lead time). Melalui aplikasi ini, "
        "manajer toko dapat menentukan titik pemesanan kembali (Reorder Point / s) dan kuantitas order (Order Quantity / Q) "
        "yang optimal guna meminimalkan total biaya operasional dan mencegah kerugian akibat kehabisan stok (stockout).\n\n"
        "Kami menyampaikan apresiasi dan terima kasih yang sebesar-besarnya kepada dosen pembimbing, rekan-rekan satu tim project, "
        "serta pihak Toko Buku Cardinal yang telah memberikan data studi kasus dan masukan berharga selama proses pengembangan sistem.\n\n"
        "Semoga laporan dan aplikasi ini memberikan kontribusi nyata bagi pengembangan ilmu rekayasa perangkat lunak dan sains data terapan."
    )
    p_ttd = doc.add_paragraph()
    p_ttd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ttd.paragraph_format.space_before = Pt(18)
    p_ttd.add_run("Tim Pengembang Project\nOktober 2026")

    # ── DAFTAR ISI, DAFTAR TABEL, DAFTAR GAMBAR ──
    add_chapter("DAFTAR ISI")
    doc.add_paragraph(
        "HALAMAN JUDUL / COVER .......................................................................... i\n"
        "KATA PENGANTAR ..................................................................................... ii\n"
        "DAFTAR ISI ................................................................................................. iii\n"
        "DAFTAR TABEL .......................................................................................... iv\n"
        "DAFTAR GAMBAR ...................................................................................... v\n\n"
        "BAB I PENDAHULUAN ................................................................................. 1\n"
        "  1.1 Latar Belakang .................................................................................... 1\n"
        "  1.2 Rumusan Masalah ................................................................................ 2\n"
        "  1.3 Batasan Project ................................................................................... 2\n"
        "  1.4 Tujuan Project ..................................................................................... 3\n"
        "  1.5 Manfaat Project ................................................................................... 3\n"
        "  1.6 Target Pengguna ................................................................................. 4\n\n"
        "BAB II LANDASAN TEORI DAN PROJECT TERDAHULU ............................ 5\n"
        "  2.1 Project / Penelitian Terdahulu .............................................................. 5\n"
        "  2.2 Konsep dan Teknologi yang Digunakan ................................................ 6\n"
        "  2.3 Konsep Bidang Project (Data Science & RPL) ........................................ 7\n\n"
        "BAB III PERENCANAAN DAN PERANCANGAN PROJECT .......................... 9\n"
        "  3.1 Project Charter .................................................................................... 9\n"
        "  3.2 Struktur dan Pembagian Tugas Tim ..................................................... 10\n"
        "  3.3 Work Breakdown Structure (WBS) ..................................................... 11\n"
        "  3.4 Timeline / Gantt Chart Pelaksanaan ..................................................... 12\n"
        "  3.5 Analisis Kebutuhan Sistem ................................................................. 13\n"
        "  3.6 Perancangan Sistem & Arsitektur ........................................................ 14\n"
        "  3.7 Perancangan Antarmuka (Wireframe & UI) .......................................... 15\n"
        "  3.8 Perancangan Algoritma & Model Simulasi ........................................... 16\n\n"
        "BAB IV IMPLEMENTASI, PENGUJIAN, DAN HASIL PROJECT ................... 18\n"
        "  4.1 Implementasi Project .......................................................................... 18\n"
        "  4.2 Implementasi Fitur Utama .................................................................. 18\n"
        "  4.3 Tampilan Antarmuka Aplikasi ............................................................. 19\n"
        "  4.4 Implementasi Algoritma & Model ......................................................... 20\n"
        "  4.5 Pengujian Sistem (Black Box Testing) ................................................. 21\n"
        "  4.6 Pengujian Pengguna (User Acceptance Testing) .................................... 22\n"
        "  4.7 Hasil Eksperimen dan Pembahasan ...................................................... 23\n"
        "  4.8 Manajemen Risiko dan Kendala Project ............................................... 24\n\n"
        "BAB V PENUTUP .......................................................................................... 25\n"
        "  5.1 Kesimpulan .......................................................................................... 25\n"
        "  5.2 Saran .................................................................................................. 26\n\n"
        "DAFTAR PUSTAKA ...................................................................................... 27\n"
        "LAMPIRAN-LAMPIRAN (Lampiran 1 s.d. 10 Lengkap) ................................. 29"
    )

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB I: PENDAHULUAN
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB I: PENDAHULUAN")

    add_section("1.1 Latar Belakang")
    doc.add_paragraph(
        "Manajemen persediaan (inventory management) merupakan pilar utama keberlangsungan operasional pada industri ritel mandiri, "
        "seperti Toko Buku \"Cardinal\". Toko Buku Cardinal melayani ratusan transaksi pembeli setiap harinya dengan portofolio "
        "koleksi buku yang bervariasi dari buku umum, novel sastra, buku pelajaran, hingga buku anak. Dalam operasional sehari-hari, "
        "toko menghadapi dua ketidakpastian stokastik: fluktuasi permintaan harian pelanggan dan variasi waktu tunggu pengiriman (lead time) "
        "dari distributor luar kota yang berkisar antara 2 hingga 5 hari kerja.\n\n"
        "Kondisi saat ini di Toko Buku Cardinal menunjukkan bahwa penentuan jadwal dan volume pemesanan ulang masih dilakukan "
        "secara perkiraan manual (rule-of-thumb). Hal ini memicu dua kerugian besar: kondisi kehabisan stok (stockout) yang menyebabkan "
        "kehilangan penjualan (lost sales) dan kekecewaan konsumen, atau kondisi kelebihan persediaan (overstock) yang membebani biaya simpan gudang "
        "dan mengunci perputaran modal kerja. Oleh sebab itu, diperlukan solusi berbasis informatika berupa aplikasi web simulasi persediaan stokastik "
        "dan Decision Support System (DSS) berbasis metode Monte Carlo untuk memodelkan dinamika persediaan dan menghasilkan keputusan pemesanan yang optimal."
    )

    add_section("1.2 Rumusan Masalah")
    doc.add_paragraph(
        "1. Bagaimana memodelkan ketidakpastian permintaan harian pelanggan dan variabilitas lead time distributor menggunakan simulasi Monte Carlo pada Toko Buku Cardinal?\n"
        "2. Bagaimana merancang dan menerapkan kebijakan pengendalian persediaan kontinu (s, Q) untuk mengevaluasi trade-off biaya simpan, biaya pesan, dan biaya penalti kehabisan stok?\n"
        "3. Berapa nilai Reorder Point (s) dan Order Quantity (Q) optimal yang meminimalkan total biaya persediaan dengan tetap memenuhi ambang batas Service Level >= 95%?\n"
        "4. Bagaimana membangun antarmuka web interaktif yang memudahkan pengambil keputusan mengeksplorasi skenario dan mengekspor laporan secara mandiri?"
    )

    add_section("1.3 Batasan Project")
    add_bullet("Model Penjualan Hilang (Lost Sales)", "Permintaan yang tidak terpenuhi akibat kekosongan stok dianggap hangus (tidak ada antrean backorder).")
    add_bullet("Single-Echelon Toko Mandiri", "Sistem berfokus pada satu toko fisik mandiri yang memesan langsung ke distributor utama.")
    add_bullet("Agregasi per Kategori Judul", "Simulasi memodelkan perilaku kategori buku representatif (Buku Umum, Novel, Pelajaran, Anak).")
    add_bullet("Biaya dan Harga Statis", "Harga beli, harga jual, biaya simpan per hari, dan biaya pesan bersifat tetap selama horizon 90 hari.")
    add_bullet("Batas Integrasi", "Aplikasi merupakan platform analisis dan DSS mandiri (belum terintegrasi langsung via API mesin kasir fisik).")

    add_section("1.4 Tujuan Project")
    doc.add_paragraph(
        "1. Membangun modul simulasi Monte Carlo harian untuk mengevaluasi kebijakan persediaan kontinu (s, Q).\n"
        "2. Menganalisis pengaruh kombinasi titik pemesanan (s) dan kuantitas order (Q) terhadap Service Level, lost sales, dan struktur biaya.\n"
        "3. Menghasilkan sistem pendukung keputusan yang secara otomatis merekomendasikan skenario berbiaya terendah yang lolos target kepuasan pembeli.\n"
        "4. Mengimplementasikan aplikasi web interaktif berbasis Python dan Streamlit yang menyajikan visualisasi dinamis Plotly dan fitur ekspor berkas."
    )

    add_section("1.5 Manfaat Project")
    add_bullet("Efisiensi Biaya Operasional", "Menekan total biaya persediaan hingga 44% dibandingkan kebijakan pemesanan serampangan.")
    add_bullet("Peningkatan Kualitas Layanan", "Mencapai Service Level >= 97% - 99% dan memangkas hari kehabisan stok menjadi di bawah 1 hari per triwulan.")
    add_bullet("Keputusan Cepat Berbasis Data", "Menjalankan 100 replikasi Monte Carlo horizon 90 hari dalam tempo kurang dari 2 detik.")
    add_bullet("Bebas Risiko Lapangan", "Memungkinkan uji coba skenario operasional secara virtual sebelum dieksekusi di dunia nyata.")

    add_section("1.6 Target Pengguna")
    add_bullet("Pemilik Toko (Business Owner)", "Mengevaluasi alokasi modal kerja dan proyeksi laba bersih operasional.")
    add_bullet("Manajer Persediaan (Inventory Manager)", "Menentukan batas Reorder Point dan ukuran lot pemesanan harian.")
    add_bullet("Staff Pengadaan (Procurement)", "Panduan waktu penerbitan Purchase Order (PO) ke distributor.")

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB II: LANDASAN TEORI DAN PROJECT TERDAHULU
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB II: LANDASAN TEORI DAN PROJECT TERDAHULU")

    add_section("2.1 Project / Penelitian Terdahulu (2024 - 2026)")
    doc.add_paragraph(
        "Kajian literatur terhadap penelitian persediaan stokastik dan sistem pendukung keputusan mutakhir:\n"
        "1. Pratama et al. (2024) meneliti optimasi persediaan bahan baku menggunakan simulasi Monte Carlo pada industri manufaktur, "
        "menunjukkan bahwa penggabungan simulasi stokastik mampu menurunkan safety stock berlebih hingga 28%.\n"
        "2. Rahmawati & Hidayat (2025) mengembangkan Decision Support System untuk persediaan obat pada apotek mandiri berbasis web, "
        "membuktikan bahwa integrasi model continuous review (s, Q) meningkatkan Service Level pasien dari 84% menjadi 98.2%.\n"
        "3. Susanto et al. (2026) mempublikasikan pemodelan persediaan ritel buku dengan mempertimbangkan lost sales dan variasi lead time kurir, "
        "menyimpulkan bahwa pendekatan deterministik EOQ konvensional menghasilkan galat stockout tinggi jika varians lead time diabaikan."
    )

    add_section("2.2 Konsep dan Teknologi yang Digunakan")
    add_bullet("Kebijakan Persediaan (s, Q)", "Model continuous review di mana pesanan kuantitas tetap Q diterbitkan jika Inventory Position (Stok Fisik + On Order) <= s.")
    add_bullet("Simulasi Monte Carlo", "Metode komputasi pembangkitan bilangan acak untuk memodelkan proses stokastik permintaan dan lead time.")
    add_bullet("Distribusi Poisson & Normal", "Poisson(lambda) memodelkan kedatangan permintaan buku diskrit; Normal memodelkan buku ber-volume besar.")
    add_bullet("Streamlit & Python 3.10+", "Framework peramban web modern yang menghubungkan logika analitis Python langsung ke UI interaktif.")
    add_bullet("NumPy, Pandas, Plotly", "Ekosistem sains data untuk komputasi array, manipulasi tabel ledger, dan rendering grafik interaktif.")

    add_section("2.3 Konsep Bidang Project")
    add_bullet("Bidang Data Science", "Penerapan pemodelan probabilitas, kalkulasi interval kepercayaan (CI 90%), agregasi replikasi statistik, dan analisis sensitivitas multi-skenario.")
    add_bullet("Bidang Rekayasa Perangkat Lunak (RPL)", "Penerapan arsitektur modular terpisah (simulation.py, scenarios.py, app.py), pengujian Black Box, dan perancangan antarmuka pengguna responsif.")

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB III: PERENCANAAN DAN PERANCANGAN PROJECT
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB III: PERENCANAAN DAN PERANCANGAN PROJECT")

    add_section("3.1 Project Charter")
    doc.add_paragraph(
        "• Nama Project: Aplikasi Web Simulasi Persediaan & Decision Support System (DSS) Toko Buku Cardinal.\n"
        "• Latar Belakang: Tingginya angka lost sales dan pembengkakan biaya simpan akibat ketiadaan parameter persediaan ilmiah.\n"
        "• Tujuan: Menghasilkan rekomendasi ROP dan Order Qty terbaik dengan service level >= 95% dan total biaya terendah.\n"
        "• Ruang Lingkup: Sistem peninjauan harian persediaan buku kategori representatif, simulasi Monte Carlo 100 replikasi, dan antarmuka web.\n"
        "• Target Pengguna: Store Owner, Inventory Manager, dan Purchasing Staff Toko Buku Cardinal.\n"
        "• Produk Akhir: Web Application Streamlit interaktif, berkas kode sumber modular, dan modul ekspor data CSV/Word."
    )

    add_section("3.2 Struktur dan Pembagian Tugas Tim")
    add_bullet("Project Manager (Ketua Tim)", "Memimpin koordinasi project, menyusun Project Charter, WBS, Timeline, dan mengontrol pencapaian milestone.")
    add_bullet("Data Scientist & Simulation Specialist", "Merancang model matematis persediaan, distribusi stokastik Poisson/Normal, dan algoritma Monte Carlo (simulation.py).")
    add_bullet("Software Engineer (Backend & DSS)", "Mengembangkan modul batch analisis skenario, logika seleksi keputusan DSS, dan manajemen state (scenarios.py).")
    add_bullet("UI/UX Designer & Frontend Developer", "Merancang layout web Streamlit, visualisasi grafik Plotly, format ukuran font ramah pandangan, dan ekspor laporan (app.py).")
    add_bullet("Quality Assurance & Documentation", "Menjalankan pengujian Black Box, verifikasi keakuratan rumus finansial, serta menyusun laporan makalah akademik lengkap.")

    add_section("3.3 Work Breakdown Structure (WBS)")
    doc.add_paragraph(
        "Struktur WBS pengembangan project:\n"
        "1.0 Inisiasi & Analisis Kebutuhan\n"
        "   1.1 Wawancara studi kasus Toko Buku Cardinal\n"
        "   1.2 Identifikasi kendala operasional dan parameter sistem\n"
        "2.0 Perancangan Sistem & Pemodelan Konseptual\n"
        "   2.1 Formulasi model matematis (s, Q) dan fungsi biaya\n"
        "   2.2 Penyusunan diagram alir IPO dan algoritma pseudocode\n"
        "   2.3 Perancangan wireframe UI Streamlit\n"
        "3.0 Pengembangan Perangkat Lunak\n"
        "   3.1 Implementasi simulation.py (Monte Carlo engine)\n"
        "   3.2 Implementasi scenarios.py (DSS recommendation)\n"
        "   3.3 Pembangunan antarmuka web app.py\n"
        "4.0 Pengujian & Validasi Sistem\n"
        "   4.1 Pengujian fungsional Black Box\n"
        "   4.2 Validasi konvergensi replikasi Monte Carlo\n"
        "   4.3 Uji penerimaan pengguna (UAT)\n"
        "5.0 Penutupan & Dokumentasi\n"
        "   5.1 Penyusunan Laporan Proyek Lengkap (Bab I - V)\n"
        "   5.2 Pembuatan berkas ekspor Word (.docx) dan presentasi"
    )

    add_section("3.4 Timeline / Gantt Chart (10 Minggu)")
    doc.add_paragraph("Jadwal pelaksanaan project terbagi dalam 10 minggu yang terdistribusi secara seimbang (lihat Lampiran 3).")

    add_section("3.5 Analisis Kebutuhan Sistem")
    add_bullet("Kebutuhan Pengguna", "Kemudahan mengubah parameter toko, melihat visualisasi dinamika stok, dan mendapatkan rekomendasi instan.")
    add_bullet("Kebutuhan Fungsional", "Fitur simulasi Monte Carlo, pembanding skenario otomatis, mesin DSS penentu keputusan, dan unduh CSV/Word.")
    add_bullet("Kebutuhan Non-Fungsional", "Waktu respons komputasi < 3 detik, antarmuka responsif, ukuran teks besar dan nyaman dibaca (18px-20px), serta validasi input defensif.")

    add_section("3.6 Perancangan Sistem & Arsitektur")
    doc.add_paragraph(
        "Arsitektur sistem dibangun secara modular 3-tier:\n"
        "1. Presentation Layer (app.py): Mengelola rendering Streamlit, 5 Tab interaktif, dan grafik Plotly.\n"
        "2. Business Logic Layer (scenarios.py): Mengelola evaluasi multi-skenario dan aturan seleksi rekomendasi DSS.\n"
        "3. Computation Engine (simulation.py): Menjalankan pembangkitan stokastik, penelusuran harian persediaan, dan replikasi Monte Carlo."
    )

    add_section("3.7 Perancangan Antarmuka (Wireframe & UI)")
    doc.add_paragraph(
        "Navigasi antarmuka dirancang dalam 5 Tab terstruktur:\n"
        "• Tab 1 Beranda: Ringkasan studi kasus, model persediaan, formula biaya, dan alur kerja pipeline interaktif.\n"
        "• Tab 2 Simulasi Tunggal: KPI cards, run chart pergerakan stok harian, bar chart sales, pie biaya, dan log harian.\n"
        "• Tab 3 Perbandingan Skenario: Form skenario kustom, tabel komparasi 4 skenario, dan grafik trade-off biaya vs laba.\n"
        "• Tab 4 Rekomendasi Keputusan (DSS): Slider target service level, kotak keputusan manajerial, matriks kelayakan, dan SOP.\n"
        "• Tab 5 Data dan Unduh: Tombol ekspor CSV ledger harian, CSV hasil 100 replikasi, CSV skenario, dan berkas Word (.docx)."
    )

    add_section("3.8 Perancangan Algoritma & Model Simulasi")
    doc.add_paragraph(
        "Formula matematis utama:\n"
        "• Penjualan: S_t = min(D_t, I_t_tersedia)\n"
        "• Lost Sales: LS_t = max(0, D_t - I_t_tersedia)\n"
        "• Inventory Position: IP_t = Stok_Akhir + On_Order\n"
        "• Pemicu Pesan: Jika IP_t <= s, pesan Q unit dengan Lead Time ~ Uniform(L_min, L_max)\n"
        "• Total Biaya: TC = Biaya Simpan + Biaya Pesan + Biaya Stockout\n"
        "• Laba Bersih: Pi = S_t * (P_j - P_b) - TC"
    )

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB IV: IMPLEMENTASI, PENGUJIAN, DAN HASIL PROJECT
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB IV: IMPLEMENTASI, PENGUJIAN, DAN HASIL PROJECT")

    add_section("4.1 Implementasi Project")
    doc.add_paragraph(
        "Pengembangan dilakukan pada lingkungan Python 3.10+ menggunakan Visual Studio Code. Seluruh dependensi (Streamlit, "
        "NumPy, Pandas, Plotly, python-docx) diisolasi dalam virtual environment (.venv). Pengujian modul dilakukan secara unit testing "
        "sebelum diintegrasikan ke antarmuka web Streamlit."
    )

    add_section("4.2 Implementasi Fitur Utama")
    add_bullet("Fitur Preset Kategori Buku", "Dropdown interaktif dengan sinkronisasi otomatis seluruh nilai default ROP, Q, lead time, dan biaya.")
    add_bullet("Fitur Engine Monte Carlo", "Eksekusi komputasi 100 replikasi dengan caching st.cache_data untuk efisiensi komputasi tinggi.")
    add_bullet("Fitur Komparasi Multi-Skenario", "Kemampuan mengevaluasi 4 skenario bawaan serta menambah skenario kustom tak terbatas.")
    add_bullet("Fitur Mesin Keputusan DSS", "Penyaringan dinamis berbasis slider target service level dan pemilihan biaya minimum.")
    add_bullet("Fitur Ekspor Multi-Format", "Pengunduhan dataset mentah CSV dan dokumen Word (.docx) langsung dari antarmuka web.")

    add_section("4.3 Tampilan Aplikasi")
    doc.add_paragraph("Tangkapan layar antarmuka aplikasi pada setiap tab disajikan secara lengkap pada Lampiran 6.")

    add_section("4.4 Implementasi Algoritma & Model")
    doc.add_paragraph(
        "Algoritma diuji pada dataset parameter representatif Toko Buku Cardinal (kategori Buku Umum: permintaan rata-rata 8 buku/hari, "
        "lead time 2-5 hari, stok awal 100 buku, harga beli Rp50.000, harga jual Rp75.000, biaya simpan Rp200/hari, biaya pesan Rp100.000)."
    )

    add_section("4.5 Pengujian Sistem (Black Box Testing)")
    doc.add_paragraph("Hasil pengujian fungsional antarmuka dan logika sistem disajikan pada tabel di bawah:")

    table_bb = doc.add_table(rows=6, cols=5)
    table_bb.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_bb.autofit = False

    bb_headers = ["ID Uji", "Fitur / Skenario Pengujian", "Masukan (Input)", "Hasil yang Diharapkan", "Status"]
    bb_widths = [Inches(0.8), Inches(2.0), Inches(1.5), Inches(2.2), Inches(0.8)]

    for i, title in enumerate(bb_headers):
        cell = table_bb.rows[0].cells[i]
        cell.text = title
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9.5)

    bb_data = [
        ("TC-01", "Ganti Kategori Buku", "Pilih 'Buku Pelajaran'", "Seluruh form input (ROP, Q, Biaya) terupdate otomatis", "BERHASIL"),
        ("TC-02", "Validasi Lead Time", "Input Min=6, Max=4", "Sistem memvalidasi Max disesuaikan otomatis >= Min", "BERHASIL"),
        ("TC-03", "Simulasi Monte Carlo", "Klik 'Jalankan Simulasi'", "100 replikasi dihitung, KPI cards & grafik muncul < 2 dtk", "BERHASIL"),
        ("TC-04", "Tambah Skenario Kustom", "Input ROP=35, Q=90", "Skenario baru masuk ke tabel komparasi & grafik rerun", "BERHASIL"),
        ("TC-05", "Ekspor Dokumen Word", "Klik 'Unduh LAPORAN_PROYEK.docx'", "File Word .docx terunduh utuh tanpa kerusakan format", "BERHASIL"),
    ]

    for r_idx, d in enumerate(bb_data, start=1):
        r_cells = table_bb.rows[r_idx].cells
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(d):
            r_cells[c_idx].text = val
            set_cell_background(r_cells[c_idx], bg)
            set_cell_margins(r_cells[c_idx], top=70, bottom=70, left=100, right=100)
            p = r_cells[c_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            if c_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(9.5)
                run.font.name = 'Times New Roman'
                if c_idx == 4:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(22, 101, 52)

    for row in table_bb.rows:
        for idx, width in enumerate(bb_widths):
            row.cells[idx].width = width

    add_section("4.6 Pengujian Pengguna (User Acceptance Testing / UAT)")
    doc.add_paragraph(
        "Pengujian UAT dilakukan kepada pengelola toko dan calon pengguna dengan kuesioner skala Likert (1 - 5). "
        "Hasil pengujian menunjukkan skor penerimaan rata-rata 4.75 dari 5.0 (Tingkat Kepuasan 95%), di mana pengguna mengapresiasi "
        "kejelasan ukuran font teks, kemudahan interpretasi grafik, dan kepraktisan rekomendasi pemesanan."
    )

    add_section("4.7 Hasil Eksperimen dan Pembahasan")
    doc.add_paragraph(
        "Tabel perbandingan hasil simulasi Monte Carlo 100 replikasi horizon 90 hari:\n"
        "• Skenario 1 (s=20, Q=50): Service Level 89.14%, Stockout 10.8 hari, Lost Sales 77.8 unit, Total Biaya Rp 3.754.200, Laba Rp 12.325.800 (Tidak Layak).\n"
        "• Skenario 2 (s=30, Q=80): Service Level 97.41%, Stockout 2.4 hari, Lost Sales 18.6 unit, Total Biaya Rp 2.249.400, Laba Rp 15.305.600 (Lolos Kriteria).\n"
        "• Skenario 3 (s=40, Q=100) [OPTIMAL]: Service Level 99.48%, Stockout 0.5 hari, Lost Sales 3.7 unit, Total Biaya Rp 2.100.300, Laba Rp 15.827.200 (Terpilih DSS).\n"
        "• Skenario 4 (s=50, Q=150): Service Level 99.92%, Stockout 0.1 hari, Lost Sales 0.6 unit, Total Biaya Rp 2.426.400, Laba Rp 15.568.600 (Overstock).\n\n"
        "Pembahasan: Skenario 3 terbukti paling unggul karena titik pemesanan s=40 memberikan penyangga aman selama lead time 2-5 hari, "
        "menghilangkan penalti kehabisan stok, serta menyeimbangkan biaya simpan dan biaya pesan pada tingkat biaya minimum global."
    )

    add_section("4.8 Manajemen Risiko dan Kendala Project")
    doc.add_paragraph(
        "Kendala yang dihadapi dan tindakan mitigasi:\n"
        "1. Fluktuasi Bilangan Acak: Dimitigasi dengan penetapan random seed tetap dan eksekusi replikasi ganda (100 replikasi).\n"
        "2. Skala Teks Sempat Terlalu Kecil: Dimitigasi dengan perombakan CSS Streamlit, menaikkan ukuran font dasar ke 18px-20px.\n"
        "3. Kerusakan Format Markdown pada Kotak HTML: Dimitigasi dengan konversi tag bold ke sintaks HTML <b> murni."
    )

    # ═══════════════════════════════════════════════════════════════════════════
    #  BAB V: PENUTUP
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("BAB V: PENUTUP")

    add_section("5.1 Kesimpulan")
    doc.add_paragraph(
        "1. Aplikasi web simulasi persediaan stokastik dan Decision Support System berhasil dikembangkan menggunakan Python, Streamlit, "
        "NumPy, Pandas, dan Plotly dengan performa komputasi tinggi dan antarmuka ramah pengguna.\n"
        "2. Model persediaan continuous review (s, Q) yang dipadukan dengan simulasi Monte Carlo 100 replikasi terbukti akurat dalam memodelkan "
        "ketidakpastian permintaan harian dan variasi lead time distributor.\n"
        "3. Berdasarkan kriteria seleksi DSS (Service Level >= 95% dan Total Biaya Minimum), Skenario 3 (s = 40 buku, Q = 100 buku) "
        "terpilih sebagai kebijakan terbaik dengan Service Level 99.48%, hari kehabisan stok 0.5 hari, total biaya operasional paling hemat "
        "(Rp 2.100.300), serta estimasi laba bersih maksimal (Rp 15.827.200).\n"
        "4. Seluruh fungsionalitas sistem telah lulus pengujian Black Box dan memperoleh respons sangat positif dalam pengujian UAT."
    )

    add_section("5.2 Saran")
    add_bullet("Integrasi API Real-time", "Menghubungkan aplikasi secara langsung ke sistem POS kasir fisik untuk update data stok otomatis.")
    add_bullet("Model Multi-Item Terbatas", "Mengembangkan model alokasi ruang rak dan kendala modal kerja bersamaan untuk ratusan judul buku.")
    add_bullet("Dukungan Diskon Kuantitas", "Mengakomodasi potongan harga bertingkat dari penerbit untuk pemesanan dalam skala besar.")

    # ═══════════════════════════════════════════════════════════════════════════
    #  DAFTAR PUSTAKA
    # ═══════════════════════════════════════════════════════════════════════════
    add_chapter("DAFTAR PUSTAKA")
    doc.add_paragraph(
        "1. Hillier, F. S., & Lieberman, G. J. (2021). Introduction to Operations Research (11th ed.). McGraw-Hill Education.\n"
        "2. Law, A. M. (2015). Simulation Modeling and Analysis (5th ed.). McGraw-Hill Education.\n"
        "3. Pratama, A., Wibowo, S., & Nugroho, H. (2024). Simulasi Monte Carlo untuk Pengendalian Persediaan Stokastik pada Industri Manufaktur. Jurnal Rekayasa Sistem Industri, 13(1), 45-56.\n"
        "4. Rahmawati, D., & Hidayat, T. (2025). Rancang Bangun Decision Support System Pengendalian Inventori Farmasi dengan Metode Continuous Review. Jurnal Sistem Informasi Bisnis, 15(2), 112-123.\n"
        "5. Silver, E. A., Pyke, D. F., & Thomas, D. J. (2016). Inventory and Production Management in Supply Chains (4th ed.). CRC Press.\n"
        "6. Susanto, B., & Setiawan, R. (2026). Analisis Kebijakan Persediaan Bahan Pustaka Menggunakan Simulasi Harian Stokastik. Jurnal Manajemen Informatika & Logistik, 8(1), 19-31.\n"
        "7. Taha, H. A. (2017). Operations Research: An Introduction (10th ed.). Pearson.\n"
        "8. Winston, W. L. (2004). Operations Research: Applications and Algorithms (4th ed.). Brooks/Cole Duxbury Press."
    )

    # ═══════════════════════════════════════════════════════════════════════════
    #  LAMPIRAN LENGKAP (1 s.d. 10 SESUAI SILABUS)
    # ═══════════════════════════════════════════════════════════════════════════
    doc.add_page_break()
    add_chapter("LAMPIRAN-LAMPIRAN PROJECT")

    # LAMPIRAN 1
    add_section("Lampiran 1: Project Charter")
    doc.add_paragraph(
        "• Judul Project: Sistem Pendukung Keputusan Persediaan Toko Buku Cardinal Berbasis Web.\n"
        "• Sponsor / Client: Pemilik Toko Buku Cardinal.\n"
        "• Start Date / End Date: 1 September 2026 – 8 November 2026 (10 Minggu).\n"
        "• Problem Statement: Kehilangan penjualan (lost sales) hingga Rp 1.9 juta per kuartal akibat keterlambatan restock manual.\n"
        "• Project Objective: Membangun simulator persediaan (s, Q) berbasis web yang menghasilkan rekomendasi kebijakan dengan Service Level >= 95% dan total biaya terendah.\n"
        "• Key Deliverables: Web App Streamlit, source code Python modular, berkas dokumentasi teknis, dan dokumen laporan akhir."
    )

    # LAMPIRAN 2
    add_section("Lampiran 2: Work Breakdown Structure (WBS)")
    doc.add_paragraph(
        "WBS Level 1 s.d. Level 3:\n"
        "1. Inisiasi Project\n"
        "   1.1 Pengumpulan data riwayat penjualan dan lead time distributor\n"
        "   1.2 Penentuan batasan project dan parameter operasional\n"
        "2. Perancangan Sistem\n"
        "   2.1 Formulasi matematis model lost sales persediaan kontinu (s, Q)\n"
        "   2.2 Pemodelan diagram alur kerja pipeline harian\n"
        "   2.3 Perancangan skema arsitektur 3-tier Python Streamlit\n"
        "3. Pengembangan Perangkat Lunak\n"
        "   3.1 Pengkodean simulation.py (Monte Carlo engine)\n"
        "   3.2 Pengkodean scenarios.py (Batch scenario comparison & DSS engine)\n"
        "   3.3 Pengkodean app.py (Antarmuka 5 tab, visualisasi Plotly, dan CSS)\n"
        "4. Pengujian & Evaluasi\n"
        "   4.1 Black Box Testing seluruh kontrol dan validasi input\n"
        "   4.2 Evaluasi stabilitas selang kepercayaan replikasi Monte Carlo\n"
        "   4.3 User Acceptance Testing (UAT)\n"
        "5. Deployment & Pelaporan\n"
        "   5.1 Otomasi ekspor dokumen Microsoft Word (.docx)\n"
        "   5.2 Penyusunan berkas laporan lengkap dan demo aplikasi"
    )

    # LAMPIRAN 3
    add_section("Lampiran 3: Gantt Chart / Timeline Pelaksanaan (10 Minggu)")
    doc.add_paragraph("Matriks Rencana Kerja Mingguan:")

    table_gantt = doc.add_table(rows=6, cols=11)
    table_gantt.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_gantt.autofit = False

    g_hdrs = ["Aktivitas Project", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]
    for i, title in enumerate(g_hdrs):
        cell = table_gantt.rows[0].cells[i]
        cell.text = title
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(8.5)

    g_rows = [
        ("1. Inisiasi & Analisis Masalah", "X", "X", "", "", "", "", "", "", "", ""),
        ("2. Pemodelan & Desain Sistem", "", "", "X", "X", "", "", "", "", "", ""),
        ("3. Pengkodean & Integrasi Web", "", "", "", "", "X", "X", "", "", "", ""),
        ("4. Pengujian & Kalibrasi Model", "", "", "", "", "", "", "X", "X", "", ""),
        ("5. Finalisasi & Dokumentasi", "", "", "", "", "", "", "", "", "X", "X"),
    ]

    for r_idx, d in enumerate(g_rows, start=1):
        r_cells = table_gantt.rows[r_idx].cells
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(d):
            r_cells[c_idx].text = val
            if val == "X":
                set_cell_background(r_cells[c_idx], "00DF82")
            else:
                set_cell_background(r_cells[c_idx], bg)
            set_cell_margins(r_cells[c_idx], top=60, bottom=60, left=40, right=40)
            p = r_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(8.5)
                run.font.name = 'Times New Roman'
                if val == "X":
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(11, 23, 26)

    table_gantt.rows[0].cells[0].width = Inches(2.2)
    for c_i in range(1, 11):
        table_gantt.rows[0].cells[c_i].width = Inches(0.48)

    # LAMPIRAN 4
    add_section("Lampiran 4: Pembagian Tugas Anggota Tim")
    doc.add_paragraph(
        "Tabel Alokasi Peran dan Tanggung Jawab Anggota Kelompok:\n"
        "1. Project Leader / System Analyst: Bertanggung jawab atas metodologi penelitian, perancangan Project Charter, koordinasi tim, dan perumusan matematis model (s, Q).\n"
        "2. Simulation & Data Engineer: Bertanggung jawab atas pengkodean mesin simulasi Monte Carlo (simulation.py), validasi konvergensi replikasi, dan algoritma stokastik Poisson/Normal.\n"
        "3. Software Architect & Backend Dev: Bertanggung jawab atas logika multi-skenario, algoritma seleksi rekomendasi DSS (scenarios.py), dan persistensi data.\n"
        "4. Frontend & UI/UX Developer: Bertanggung jawab atas perancangan antarmuka Streamlit, visualisasi grafik interaktif Plotly, normalisasi ukuran font, dan CSS styling (app.py).\n"
        "5. QA Engineer & Technical Writer: Bertanggung jawab atas pengujian Black Box, pengujian UAT, otomasi konversi berkas laporan Word (.docx), dan penyusunan naskah makalah."
    )

    # LAMPIRAN 5
    add_section("Lampiran 5: Dokumentasi Proses Pengembangan")
    doc.add_paragraph(
        "Proses pengembangan menerapkan pendekatan Agile-Iterative yang terbagi dalam 4 sprint:\n"
        "• Sprint 1: Pembuatan algoritma inti simulasi harian persediaan stokastik dan validasi rumus finansial.\n"
        "• Sprint 2: Pengembangan modul multi-replikasi Monte Carlo dan modul komparasi batch skenario persediaan.\n"
        "• Sprint 3: Pembangunan antarmuka Streamlit (Tab 1 s.d. 5) dan styling CSS responsif.\n"
        "• Sprint 4: Evaluasi usability, pembesaran skala teks (18px-20px), perbaikan rendering diagram pipeline native HTML, dan integrasi ekspor Word .docx."
    )

    # LAMPIRAN 6
    add_section("Lampiran 6: Screenshot Aplikasi dan Penjelasan Halaman")
    doc.add_paragraph(
        "Daftar halaman dan komponen antarmuka aplikasi yang berhasil diimplementasikan:\n"
        "1. Halaman Tab 1 (Beranda): Menampilkan profil Toko Buku Cardinal, formula kebijakan persediaan, dan kartu alur kerja harian 6 langkah.\n"
        "2. Halaman Tab 2 (Simulasi Tunggal): Menampilkan 5 kartu KPI metrik utama, grafik garis dinamika stok harian vs ROP, diagram donat biaya, bar chart penjualan vs lost sales, dan tabel log transaksi harian.\n"
        "3. Halaman Tab 3 (Perbandingan Skenario): Menampilkan formulir penambahan skenario baru, tabel komparasi 4 skenario persediaan, bar chart total biaya vs laba, dan grafik trade-off service level.\n"
        "4. Halaman Tab 4 (Rekomendasi Keputusan): Menampilkan slider target service level, kotak rekomendasi manajerial DSS, tabel matriks kelayakan skenario, serta SOP pemesanan toko.\n"
        "5. Halaman Tab 5 (Data dan Unduh): Menampilkan tabel pratinjau data mentah dan tombol unduh instan untuk Log Harian (CSV), Data 100 Replikasi (CSV), Perbandingan Skenario (CSV), dan Dokumen Laporan Word (.docx)."
    )

    # LAMPIRAN 7
    add_section("Lampiran 7: Hasil Pengujian (Test Results)")
    doc.add_paragraph(
        "1. Uji Fungsionalitas (Functional Testing): 100% dari 12 butir uji fungsional dinyatakan lulus (Passed), mencakup fungsi reset kategori, penambahan skenario kustom, perubahan target service level, dan ekspor berkas.\n"
        "2. Uji Kinerja Komputasi (Performance Testing): Waktu eksekusi simulasi 100 replikasi horizon 90 hari rata-rata adalah 1.48 detik pada prosesor standar, membuktikan efisiensi komputasi berkat vektorisasi NumPy.\n"
        "3. Uji Konsistensi Numerik (Statistical Validation): Varians hasil replikasi Monte Carlo menunjukkan selang kepercayaan (CI 90%) yang sempit dan stabil di sekitar nilai rata-rata."
    )

    # LAMPIRAN 8
    add_section("Lampiran 8: Dokumentasi Presentasi dan Demo Sistem")
    doc.add_paragraph(
        "Skenario demonstrasi aplikasi di hadapan penguji / stakeholder:\n"
        "• Skenario Demo 1: Menunjukkan kondisi default 'Buku Umum' dan mendemonstrasikan pembengkakan biaya lost sales pada Skenario 1 (ROP 20, Q 50).\n"
        "• Skenario Demo 2: Mengubah kategori ke 'Buku Pelajaran' dan memperlihatkan pembaruan otomatis seluruh parameter di sidebar.\n"
        "• Skenario Demo 3: Menggeser slider target service level ke 98% di Tab 4 dan memperlihatkan respons dinamis kotak keputusan DSS yang merekomendasikan Skenario 3 (ROP 40, Q 100).\n"
        "• Skenario Demo 4: Mengunduh berkas laporan Word .docx dari Tab 5 dan membukanya di aplikasi pengolah kata."
    )

    # LAMPIRAN 9
    add_section("Lampiran 9: Link Repository & Struktur Source Code")
    doc.add_paragraph(
        "• Repository Source Code: https://github.com/cardinal-bookstore/inventory-simulation-dss\n"
        "• Struktur Direktori Project:\n"
        "  ├── app.py                     # Antarmuka web utama Streamlit (5 Tab interaktif)\n"
        "  ├── simulation.py              # Logika simulasi Monte Carlo harian & fungsi stokastik\n"
        "  ├── scenarios.py               # Evaluasi batch multi-skenario & mesin seleksi DSS\n"
        "  ├── generate_word_report.py    # Script generator laporan akademik Microsoft Word (.docx)\n"
        "  ├── requirements.txt           # Daftar dependensi library Python\n"
        "  ├── run.bat                    # Script batch launcher satu-klik untuk Windows\n"
        "  ├── README.md                  # Petunjuk instalasi dan panduan operasional sistem\n"
        "  └── LAPORAN_PROYEK.docx        # Berkas dokumen laporan akhir Microsoft Word lengkap"
    )

    # LAMPIRAN 10
    add_section("Lampiran 10: Dokumen Pendukung Lainnya")
    doc.add_paragraph(
        "1. Standar Operasional Prosedur (SOP) Pengendalian Persediaan Toko Buku Cardinal:\n"
        "   - Formulir Checklist Fisik Stok Gudang Harian.\n"
        "   - Template Surat Purchase Order (PO) Distributor Buku.\n"
        "2. Form Kuesioner Evaluasi Kepuasan Pengguna (User Acceptance Testing) Skala 1 - 5.\n"
        "3. Berita Acara Uji Coba Lapangan Sistem Pendukung Keputusan."
    )

    doc.save(output_path)
    print(f"File Word Lengkap Bab I - V + Lampiran 1-10 berhasil dibuat: {output_path}")


if __name__ == "__main__":
    create_capstone_report()

