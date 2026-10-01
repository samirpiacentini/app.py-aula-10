from PIL import Image
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from services.cv_engine import ComputerVisionEngine
from services.storage_service import StorageService
from repositories.analysis_repository import AnalysisRepository
from models.analysis import ImageAnalysis
from utils.logger import logger

class MainController:
    """Controlador central para integrar a Interface aos Serviços e ao Repositório."""

    def __init__(self):
        self.cv_engine = ComputerVisionEngine()

    def process_and_save_capture(self, pil_image: Image.Image, db: Session) -> ImageAnalysis:
        """Fluxo completo: Análise -> Salvamento de Imagem em Disco -> Salvamento no Banco."""
        # 1. Executa a visão computacional
        analysis_res = self.cv_engine.analyze(pil_image)

        # 2. Salva o arquivo de imagem
        image_path = StorageService.save_image(pil_image)

        # 3. Monta o payload para o banco
        payload = {
            "image_path": image_path,
            "descricao": analysis_res["descricao"],
            "objetos": analysis_res["objetos"],
            "quantidade_pessoas": analysis_res["quantidade_pessoas"],
            "rostos": analysis_res["rostos"],
            "idade": analysis_res["idade"],
            "emocao": analysis_res["emocao"],
            "cores": analysis_res["cores"],
            "luminosidade": analysis_res["luminosidade"],
            "nitidez": analysis_res["nitidez"],
            "json_resultado": analysis_res["json_resultado"]
        }

        # 4. Grava no PostgreSQL
        return AnalysisRepository.create(db, payload)

    def fetch_history(
        self, 
        db: Session, 
        query: Optional[str] = None, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> List[ImageAnalysis]:
        """Recupera histórico com suporte a filtros."""
        return AnalysisRepository.get_all(db, search_query=query, start_date=start_date, end_date=end_date)

    def delete_record(self, db: Session, record_id: int, image_path: str) -> bool:
        """Remove registro do banco de dados e apaga o arquivo físico do disco."""
        db_deleted = AnalysisRepository.delete_by_id(db, record_id)
        if db_deleted:
            StorageService.delete_image(image_path)
            return True
        return False