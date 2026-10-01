import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List

from utils.logger import logger


class ComputerVisionEngine:
    """Pipeline de processamento e análise de imagens via OpenCV e NumPy."""

    def __init__(self):
        self.face_cascade = None

        try:
            cascade_path = (
                cv2.data.haarcascades
                + "haarcascade_frontalface_default.xml"
            )

            self.face_cascade = cv2.CascadeClassifier(cascade_path)

            if self.face_cascade.empty():
                logger.warning(
                    "O arquivo Haar Cascade não pôde ser carregado."
                )
                self.face_cascade = None

        except Exception as e:
            logger.error(
                f"Erro ao inicializar o CascadeClassifier: {e}"
            )
            self.face_cascade = None

    def analyze(self, pil_image: Image.Image) -> Dict[str, Any]:
        """Executa a análise completa da imagem."""

        try:
            # PIL -> NumPy
            image = np.array(pil_image)

            # RGB/RGBA -> BGR
            if len(image.shape) == 3 and image.shape[2] == 3:
                cv_image = cv2.cvtColor(
                    image,
                    cv2.COLOR_RGB2BGR
                )

            elif len(image.shape) == 3 and image.shape[2] == 4:
                cv_image = cv2.cvtColor(
                    image,
                    cv2.COLOR_RGBA2BGR
                )

            else:
                cv_image = image

            height, width = cv_image.shape[:2]

            # Escala de cinza
            if len(cv_image.shape) == 2:
                gray = cv_image
            else:
                gray = cv2.cvtColor(
                    cv_image,
                    cv2.COLOR_BGR2GRAY
                )

            # -----------------------------
            # 1. DETECÇÃO DE ROSTOS
            # -----------------------------

            faces = []

            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

            num_faces = len(faces)

            # -----------------------------
            # 2. QUALIDADE DA IMAGEM
            # -----------------------------

            luminosity = float(np.mean(gray))

            sharpness = float(
                cv2.Laplacian(
                    gray,
                    cv2.CV_64F
                ).var()
            )

            # -----------------------------
            # 3. CORES
            # -----------------------------

            if len(cv_image.shape) == 3:
                dominant_colors = self._extract_dominant_colors(
                    cv_image
                )
            else:
                dominant_colors = ["Imagem em escala de cinza"]

            # -----------------------------
            # 4. CARACTERÍSTICAS
            # -----------------------------

            objects_detected = self._detect_basic_features(
                gray,
                num_faces
            )

            # -----------------------------
            # 5. DESCRIÇÃO
            # -----------------------------

            description = self._generate_description(
                width,
                height,
                num_faces,
                luminosity,
                sharpness
            )

            # -----------------------------
            # 6. RESULTADO
            # -----------------------------

            result = {
                "descricao": description,

                "objetos": ", ".join(
                    objects_detected
                ),

                "quantidade_pessoas": num_faces,

                "rostos": num_faces,

                "idade": (
                    "Não estimada"
                ),

                "emocao": (
                    "Não estimada"
                ),

                "cores": ", ".join(
                    dominant_colors
                ),

                "luminosidade": round(
                    luminosity,
                    2
                ),

                "nitidez": round(
                    sharpness,
                    2
                ),

                "resolucao": f"{width}x{height}",

                "json_resultado": {
                    "width": width,
                    "height": height,

                    "face_coordinates": [
                        [
                            int(x),
                            int(y),
                            int(w),
                            int(h)
                        ]
                        for (
                            x,
                            y,
                            w,
                            h
                        ) in faces
                    ],

                    "status_processamento": "Sucesso",

                    "extensibilidade": (
                        "Pronto para integração "
                        "com modelos de visão."
                    )
                }
            }

            logger.info(
                "Análise de visão computacional "
                "concluída com sucesso."
            )

            return result

        except Exception as e:

            logger.error(
                f"Erro durante a análise: {e}"
            )

            raise

    def _extract_dominant_colors(
        self,
        bgr_image: np.ndarray,
        num_colors: int = 3
    ) -> List[str]:

        pixels = bgr_image.reshape(-1, 3)

        counts = np.bincount(
            pixels.dot(
                np.array(
                    [1, 256, 256 ** 2],
                    dtype=np.int64
                )
            )
        )

        top_indices = np.argsort(
            counts
        )[-num_colors:][::-1]

        colors = []

        for idx in top_indices:

            b = idx % 256
            g = (idx // 256) % 256
            r = (idx // (256 ** 2)) % 256

            colors.append(
                f"RGB({r},{g},{b})"
            )

        return colors

    def _detect_basic_features(
        self,
        gray_image: np.ndarray,
        num_faces: int
    ) -> List[str]:

        features = []

        if num_faces > 0:

            features.append(
                f"{num_faces} rosto(s) humano(s)"
            )

        edges = cv2.Canny(
            gray_image,
            100,
            200
        )

        edge_density = (
            np.sum(edges > 0)
            / edges.size
        )

        if edge_density > 0.15:

            features.append(
                "Cena detalhada / texturizada"
            )

        else:

            features.append(
                "Fundo suave / minimalista"
            )

        return features

    def _generate_description(
        self,
        width: int,
        height: int,
        faces: int,
        luminosity: float,
        sharpness: float
    ) -> str:

        lighting = (
            "boa iluminação"
            if luminosity > 100
            else "baixa luminosidade"
        )

        focus = (
            "alta nitidez"
            if sharpness > 100
            else "foco suave/desfocado"
        )

        if faces > 0:

            return (
                f"Captura ({width}x{height}) "
                f"contendo {faces} pessoa(s), "
                f"apresentando {lighting} "
                f"e {focus}."
            )

        return (
            f"Cena ampla ({width}x{height}) "
            f"sem presença identificada de rostos, "
            f"com {lighting} e {focus}."
        )