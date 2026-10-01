from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.settings import DATABASE_URL
from models.base import Base
from utils.logger import logger

# Configuração da Engine tratando pooling de conexão para Neon.tech (serverless PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> bool:
    """Cria automaticamente as tabelas no banco de dados se não existirem."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado e tabelas verificadas.")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        return False

def get_db():
    """Gerador de sessão para interações contextuais com o banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()