import json
from pathlib import Path
from typing import Any, Dict, Optional

from utils.logger import logger


class StorageService:
    """Responsável por salvar e carregar resultados das análises."""

    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = Path(storage_dir)

        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            f"StorageService iniciado em: {self.storage_dir}"
        )

    def save_json(
        self,
        data: Dict[str, Any],
        filename: str = "resultado.json"
    ) -> str:

        try:
            file_path = self.storage_dir / filename

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            logger.info(
                f"Resultado salvo em: {file_path}"
            )

            return str(file_path)

        except Exception as e:

            logger.error(
                f"Erro ao salvar resultado: {e}"
            )

            raise

    def load_json(
        self,
        filename: str = "resultado.json"
    ) -> Optional[Dict[str, Any]]:

        try:

            file_path = self.storage_dir / filename

            if not file_path.exists():

                logger.warning(
                    f"Arquivo não encontrado: {file_path}"
                )

                return None

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception as e:

            logger.error(
                f"Erro ao carregar resultado: {e}"
            )

            raise

    def exists(
        self,
        filename: str
    ) -> bool:

        return (
            self.storage_dir / filename
        ).exists()
    