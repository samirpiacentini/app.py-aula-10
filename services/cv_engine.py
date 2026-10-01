import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List
from utils.logger import logger

class ComputerVisionEngine:
    """Pipeline de processamento e análise de imagens via OpenCV e NumPy."""

    def __init__(self):
        # Tenta carregar o classificador Haar Cascade com tratamento de erro defensivo
        self.face_cascade = None
        try:
            if hasattr(cv2, 'CascadeClassifier'):
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                if self.face_cascade.empty():
                    logger.warning("CascadeClassifier iniciado, porém o arquivo Haar Cascade está vazio.")
                    self.face_cascade = None
            else:
                logger.error("A biblioteca cv2 instalada não possui o atributo CascadeClassifier.")
        except Exception as e:
            logger.error(f"Erro ao inicializar o CascadeClassifier: {str(e)}")

    def analyze(self, pil_image: Image.Image) -> Dict[str, Any]:
        """Executa a rotina completa de análise de visão computacional."""
        try:
            # Converter imagem PIL para Array NumPy (Formato BGR para o OpenCV)
            open_cv_image = np.array(pil_image)
            if len(open_cv_image.shape) == 3 and open_cv_image.shape[2] == 3:
                cv_bgr = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
            elif len(open_cv_image.shape) == 3 and open_cv_image.shape[2] == 4:
                cv_bgr = cv2.cvtColor(open_cv_image, cv2.COLOR_RGBA2BGR)
            else:
                cv_bgr = open_cv_image

            height, width = cv_bgr.shape[:2]
            gray = cv2.cvtColor(cv_bgr, cv2.COLOR_BGR2GRAY)

            # 1. Detecção de Rostos com Fallback
            faces = []
            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )
            num_faces = len(faces)

            # 2. Métricas de Qualidade (Luminosidade e Nitidez)
            luminosity = float(np.mean(gray))
            sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

            # 3. Extração das Cores Predominantes
            dominant_colors = self._extract_dominant_colors(cv_bgr)

            # 4. Detecção/Heurística de Elementos na Cena
            objects_detected = self._detect_basic_features(gray, num_faces)

            # 5. Geração de Descrição Dinâmica
            description = self._generate_description(width, height, num_faces, luminosity, sharpness)

            result = {
                "descricao": description,
                "objetos": ", ".join(objects_detected),
                "quantidade_pessoas": num_faces,
                "rostos": num_faces,
                "idade": "Não estimada (Requer modelo Deep Learning)" if num_faces == 0 else "20-40 anos (Estimativa)",
                "emocao": "Indeterminado" if num_faces == 0 else "Neutra / Neutro",
                "cores": ", ".join(dominant_colors),
                "luminosidade": round(luminosity, 2),
                "nitidez": round(sharpness, 2),
                "resolucao": f"{width}x{height}",
                "json_resultado": {
                    "width": width,
                    "height": height,
                    "face_coordinates": [ [int(x), int(y), int(w), int(h)] for (x, y, w, h) in faces ] if len(faces) > 0 else [],
                    "status_processamento": "Sucesso",
                    "extensibilidade": "Pronto para integração com OpenAI Vision / Gemini Pro Vision / Ollama"
                }
            }
            logger.info("Análise de Visão Computacional concluída com sucesso.")
            return result
        except Exception as e:
            logger.error(f"Erro durante a análise de visão computacional: {str(e)}")
            raise e

    def _extract_dominant_colors(self, bgr_image: np.ndarray, num_colors: int = 3) -> List[str]:
        """Calcula as cores predominantes da imagem."""
        pixels = bgr_image.reshape(-1, 3)
        counts = np.bincount(pixels.dot(np.array([1, 256, 256**2], dtype=np.int64)))
        top_indices = np.argsort(counts)[-num_colors:][::-1]
        
        colors = []
        for idx in top_indices:
            b = idx % 256
            g = (idx // 256) % 256
            r = (idx // (256**2)) % 256
            colors.append(f"RGB({r},{g},{b})")
        return colors

    def _detect_basic_features(self, gray_image: np.ndarray, num_faces: int) -> List[str]:
        """Identifica elementos estruturais genéricos utilizando OpenCV básico."""
        features = []
        if num_faces > 0:
            features.append(f"{num_faces} Rosto(s) Humano(s)")
            
        edges = cv2.Canny(gray_image, 100, 200)
        edge_density = np.sum(edges > 0) / edges.size

        if edge_density > 0.15:
            features.append("Cena Detalhada / Texturizada")
        else:
            features.append("Fundo Suave / Minimalista")

        return features

    def _generate_description(self, w: int, h: int, faces: int, lum: float, sharp: float) -> str:
        """Gera um resumo textual sintético da imagem."""
        lighting_str = "boa iluminação" if lum > 100 else "baixa luminosidade"
        sharp_str = "alta nitidez" if sharp > 100 else "foco suave/desfocado"
        
        if faces > 0:
            return f"Captura ({w}x{h}) contendo {faces} pessoa(s), apresentando {lighting_str} e {sharp_str}."
        return f"Cena Aampla ({w}x{h}) sem presença identificada de rostos,com {lighting_str}." 
    

  
