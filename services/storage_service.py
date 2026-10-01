import json
import os
from typing import Any, Dict, List, Optional


class StorageService:
    """Serviço responsável por salvar e recuperar os resultados das análises."""

    def __init__(self, storage_path: str = "data/historico.json"):
        self.storage_path = storage_path

        directory = os.path.dirname(self.storage_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.storage_path):
            self._save_data([])

    def _load_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def save(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Salva um resultado no histórico."""
        data = self._load_data()
        data.append(resultado)
        self._save_data(data)
        return resultado

    def salvar(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Alias em português para compatibilidade."""
        return self.save(resultado)

    def get_all(self) -> List[Dict[str, Any]]:
        """Retorna todo o histórico."""
        return self._load_data()

    def listar(self) -> List[Dict[str, Any]]:
        """Alias em português para compatibilidade."""
        return self.get_all()

    def get_by_id(self, index: int) -> Optional[Dict[str, Any]]:
        """Retorna um registro pelo índice."""
        data = self._load_data()

        if 0 <= index < len(data):
            return data[index]

        return None

    def delete_all(self) -> None:
        """Apaga todo o histórico."""
        self._save_data([])

    def limpar(self) -> None:
        """Alias em português para compatibilidade."""
        self.delete_all()
