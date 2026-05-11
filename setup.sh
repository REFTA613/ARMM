#!/bin/bash

set -e

echo "[ARMM] Creazione ambiente virtuale..."

python3 -m venv venv

echo "[ARMM] Attivazione ambiente virtuale..."
source venv/bin/activate

echo "[ARMM] Aggiornamento pip..."
pip install --upgrade pip

echo "[ARMM] Installazione dipendenze..."
pip install -r requirements.txt

echo "[ARMM] Setup completato."
echo "Per usare ARMM:"
echo "source venv/bin/activate"
echo "python armm.py check"