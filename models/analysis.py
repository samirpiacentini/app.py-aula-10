from datetime import datetime
from typing import Any, Dict
from sqlalchemy import Integer, String, DateTime, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class ImageAnalysis(Base):
    """Modelo ORM para armazenar resultados da análise de visão computacional."""
    __tablename__ = "analises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    objetos: Mapped[str] = mapped_column(String(500), nullable=True)
    quantidade_pessoas: Mapped[int] = mapped_column(Integer, default=0)
    rostos: Mapped[int] = mapped_column(Integer, default=0)
    idade: Mapped[str] = mapped_column(String(50), nullable=True)
    emocao: Mapped[str] = mapped_column(String(50), nullable=True)
    cores: Mapped[str] = mapped_column(String(255), nullable=True)
    luminosidade: Mapped[float] = mapped_column(Float, nullable=False)
    nitidez: Mapped[float] = mapped_column(Float, nullable=False)
    json_resultado: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a entidade ORM em dicionário."""
        return {
            "id": self.id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "image_path": self.image_path,
            "descricao": self.descricao,
            "objetos": self.objetos,
            "quantidade_pessoas": self.quantidade_pessoas,
            "rostos": self.rostos,
            "idade": self.idade,
            "emocao": self.emocao,
            "cores": self.cores,
            "luminosidade": self.luminosidade,
            "nitidez": self.nitidez,
            "json_resultado": self.json_resultado
        }