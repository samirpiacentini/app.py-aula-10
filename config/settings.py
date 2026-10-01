import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./local.db"
)

# Garantia de compatibilidade com URLs antigas do Heroku/Neon se começarem com postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "assets" / "images"))
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_change_in_prod")

# Garantir existência do diretório de upload
os.makedirs(UPLOAD_FOLDER, exist_ok=True)