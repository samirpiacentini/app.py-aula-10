from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.analysis import ImageAnalysis
from utils.logger import logger

class AnalysisRepository:
    """Repositório responsável por operações CRUD na tabela 'analises'."""

    @staticmethod
    def create(db: Session, analysis_data: dict) -> ImageAnalysis:
        """Salva uma nova análise no banco de dados."""
        try:
            db_item = ImageAnalysis(**analysis_data)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            logger.info(f"Registro de análise #{db_item.id} inserido com sucesso.")
            return db_item
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao salvar registro de análise: {str(e)}")
            raise e

    @staticmethod
    def get_all(
        db: Session, 
        search_query: Optional[str] = None, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[ImageAnalysis]:
        """Recupera análises ordenadas por data com filtros opcionais."""
        try:
            query = db.query(ImageAnalysis)

            if search_query:
                pattern = f"%{search_query}%"
                query = query.filter(
                    (ImageAnalysis.descricao.ilike(pattern)) | 
                    (ImageAnalysis.objetos.ilike(pattern))
                )

            if start_date:
                query = query.filter(ImageAnalysis.created_at >= start_date)

            if end_date:
                query = query.filter(ImageAnalysis.created_at <= end_date)

            return query.order_by(desc(ImageAnalysis.created_at)).all()
        except Exception as e:
            logger.error(f"Erro ao carregar histórico: {str(e)}")
            return []

    @staticmethod
    def delete_by_id(db: Session, record_id: int) -> bool:
        """Remove um registro do banco de dados pelo ID."""
        try:
            record = db.query(ImageAnalysis).filter(ImageAnalysis.id == record_id).first()
            if record:
                db.delete(record)
                db.commit()
                logger.info(f"Registro #{record_id} deletado com sucesso.")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao deletar registro #{record_id}: {str(e)}")
            return False