# PowerShell script to build the executable for Windows
Set-StrictMode -Version Latest
cd $PSScriptRoot

# Create venv if not exists
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

# Activate venv
. .\.venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
python -m pip install --upgrade pip
python -m pip install -r ..\requirements.txt

# Optional: train embeddings (creates models/)
python ..\train_embeddings_svd.py

# Build single-file windowed exe including models folder
pyinstaller --onefile --windowed --add-data "models;models" ..\txt_counter_gui.py

Write-Host "Build completo. Verifica la carpeta 'dist' para el ejecutable." -ForegroundColor Green
