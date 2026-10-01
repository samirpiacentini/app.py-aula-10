import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List
from utils.logger import logger


class StorageService:
    """Serviço de armazenamento e análise de imagens."""

    def __init__(self):
        self.history = []
        self.face_cascade = None

        try:
            cascade_path = (
                cv2.data.haarcascades
                + "haarcascade_frontalface_default.xml"
            )

            self.face_cascade = cv2.CascadeClassifier(cascade_path)

            if self.face_cascade.empty():
                self.face_cascade = None

        except Exception as e:
            logger.error(f"Erro ao carregar detector de rosto: {e}")

    def analyze(self, pil_image: Image.Image) -> Dict[str, Any]:
        """Analisa uma imagem."""

        image = np.array(pil_image)

        if len(image.shape) == 3 and image.shape[2] == 3:
            cv_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        elif len(image.shape) == 3 and image.shape[2] == 4:
            cv_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        else:
            cv_image = image

        height, width = cv_image.shape[:2]

        if len(cv_image.shape) == 2:
            gray = cv_image
        else:
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        faces = []

        if self.face_cascade is not None:
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

        num_faces = len(faces)

        luminosity = float(np.mean(gray))

        sharpness = float(
            cv2.Laplacian(gray, cv2.CV_64F).var()
        )

        result = {
            "descricao": (
                f"Imagem {width}x{height} "
                f"com {num_faces} rosto(s) detectado(s)."
            ),
            "objetos": (
                f"{num_faces} rosto(s) humano(s)"
                if num_faces > 0
                else "Nenhum rosto detectado"
            ),
            "quantidade_pessoas": num_faces,
            "rostos": num_faces,
            "idade": "Não estimada",
            "emocao": "Não estimada",
            "cores": "Não calculadas",
            "luminosidade": round(luminosity, 2),
            "nitidez": round(sharpness, 2),
            "resolucao": f"{width}x{height}",
            "json_resultado": {
                "width": width,
                "height": height,
                "face_coordinates": [
                    [int(x), int(y), int(w), int(h)]
                    for x, y, w, h in faces
                ],
                "status_processamento": "Sucesso"
            }
        }

        self.history.append(result)

        return result

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def clear_history(self):
        self.history.clear()