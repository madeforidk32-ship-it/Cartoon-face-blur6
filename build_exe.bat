\
    @echo off
    REM Windows build script: create venv, install deps, download model, build with PyInstaller
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt pyinstaller requests tqdm
    python download_model.py
    pyinstaller --onefile --add-data "models;models" --hidden-import=tkinter app.py
    if exist dist\app.exe (
      echo Build succeeded: dist\app.exe
    ) else (
      echo Build failed.
    )
    pause
