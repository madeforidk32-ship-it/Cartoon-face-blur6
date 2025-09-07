# Cartoon Face Blurrer — Extreme Cartoon-Focused (Ready-to-build)

This repository prepares a **standalone Windows EXE** that blurs anime/cartoon faces using a YOLO-style
anime-face detector in ONNX format. Due to model size and licensing, the ONNX model is downloaded at build time
(script provided) from a public model repository (Hugging Face / GitHub releases).

## What you get in this package
- `app.py` — Desktop GUI (Tkinter) that loads a video, runs inference using an ONNX model, blurs detected faces, and saves output.
- `download_model.py` — Script to download a recommended ONNX model automatically.
- `requirements.txt` — Python dependencies.
- `build_exe.bat` — Windows script that installs deps and builds a single-file EXE with PyInstaller.
- `.github/workflows/build.yml` — GitHub Actions workflow to build the EXE on `windows-latest` and upload the artifact.
- `LICENSE` — MIT license placeholder.

## Important notes
- **I cannot build the EXE inside this chat environment.** However this repo is configured so you (or GitHub Actions) can produce a **single EXE** automatically.
- The recommended model (YOLOv8 anime face) will be downloaded from Hugging Face by `download_model.py`. The model file is large (often 50–400 MB).
- The GitHub Actions workflow will download the model and build the EXE for you automatically (no local setup required) if you push this repo to GitHub and enable Actions.

## Quick local build (Windows)
1. Install Python 3.10+ and Git.
2. Unzip this repo and open `PowerShell` in the folder.
3. Run (optional: create venv):
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python download_model.py
    .\build_exe.bat
    ```
4. `dist\app.exe` will be created by PyInstaller.

## GitHub Actions build (recommended)
1. Create a new GitHub repository and push this repo there.
2. The included workflow `.github/workflows/build.yml` will run on push and create a release artifact `app-windows.zip` containing the EXE.
3. Download the artifact from the Actions run page.

## Sources & models
Recommended model sources:
- `Fuyucch1/yolov8_animeface` (Hugging Face): https://huggingface.co/Fuyucch1/yolov8_animeface
- `zymk9/yolov5_anime` (GitHub): https://github.com/zymk9/yolov5_anime
- `anime-face-detector` (mmdet): https://github.com/hysts/anime-face-detector

