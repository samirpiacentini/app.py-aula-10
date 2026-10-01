import json
import pandas as pd
from typing import List
from models.analysis import ImageAnalysis

class DataExporter:
    """Utilitário para conversão do histórico em CSV ou JSON."""

    @staticmethod
    def to_csv(records: List[ImageAnalysis]) -> str:
        """Converte uma lista de entidades ImageAnalysis em uma string no formato CSV."""
        data = [r.to_dict() for r in records]
        df = pd.DataFrame(data)
        if "json_resultado" in df.columns:
            df["json_resultado"] = df["json_resultado"].apply(json.dumps)
        return df.to_csv(index=False, encoding="utf-8")

    @staticmethod
    def to_json(records: List[ImageAnalysis]) -> str:
        """Converte uma lista de entidades ImageAnalysis em JSON estruturado."""
        data = [r.to_dict() for r in records]
        return json.dumps(data, indent=4, ensure_ascii=False)