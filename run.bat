@echo off
title Simulasi Stok Toko Buku - Streamlit Launcher
echo ========================================================
echo   Menjalankan Simulasi Stok Toko Buku...
echo ========================================================
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m streamlit run app.py
) else (
    echo Menggunakan python streamlit sistem...
    python -m streamlit run app.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Terjadi kesalahan saat menjalankan aplikasi.
    pause
)
