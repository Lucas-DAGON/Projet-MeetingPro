# tests/conftest.py
import sys
from pathlib import Path

# Ajoute le dossier /src au chemin Python
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))
print("linked src path")
