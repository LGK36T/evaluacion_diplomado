# config/settings.py
from openai import OpenAI
import os
from pathlib import Path

# Carga .env si existe (forzando override)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
except Exception:
    pass

api_key = (os.getenv("OPENAI_API_KEY") or "").strip().strip('"').strip("'")

# DEBUG opcional: ver 10 primeros chars y ruta del .env
print(f"🔑 OPENAI_API_KEY = {api_key[:10]}... | .env: {env_path}")

if not api_key or not api_key.startswith("sk-"):
    raise RuntimeError("No se encontró una OPENAI_API_KEY válida en variables de entorno / .env")

client = OpenAI(api_key=api_key)
