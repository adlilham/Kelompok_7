import os
import sys
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_dir, "app.py")
    
    # Prioritaskan streamlit dari virtual environment (.venv)
    venv_streamlit = os.path.join(base_dir, ".venv", "Scripts", "streamlit.exe")
    venv_python = os.path.join(base_dir, ".venv", "Scripts", "python.exe")

    print("Memulai aplikasi Simulasi Stok Toko Buku...")
    
    if os.path.exists(venv_streamlit):
        subprocess.run([venv_streamlit, "run", app_path])
    elif os.path.exists(venv_python):
        subprocess.run([venv_python, "-m", "streamlit", "run", app_path])
    else:
        # Fallback ke streamlit bawaan environment aktif
        try:
            from streamlit.web import cli as stcli
            sys.argv = ["streamlit", "run", app_path]
            sys.exit(stcli.main())
        except ImportError:
            subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])

if __name__ == "__main__":
    main()
