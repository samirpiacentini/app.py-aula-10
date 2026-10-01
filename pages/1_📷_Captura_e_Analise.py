import streamlit as st
from PIL import Image
from database.connection import SessionLocal
from controllers.main_controller import MainController
from utils.logger import logger

st.set_page_config(page_title="Captura & Análise", page_icon="📷", layout="wide")

st.title("📷 Captura de Câmera e Análise Automática")
st.markdown("---")

col_cam, col_res = st.columns([1, 1])

with col_cam:
    st.subheader("1. Câmera")
    camera_file = st.camera_input("Acesse a câmera do dispositivo")

if camera_file is not None:
    pil_img = Image.open(camera_file)

    with col_res:
        st.subheader("2. Foto Capturada & Análise Automática")
        st.image(pil_img, caption="Foto Capturada", use_container_width=True)


        with st.spinner("Executando processamento de Visão Computacional..."):
            db = SessionLocal()
            try:
                controller = MainController()
                record = controller.process_and_save_capture(pil_img, db)
                st.success("✅ Análise executada e salva no banco de dados com sucesso!")

                st.markdown("### 📊 Resultado do Diagnóstico")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Rostos Encontrados", record.rostos)
                m2.metric("Luminosidade", f"{record.luminosidade:.1f}")
                m3.metric("Nitidez", f"{record.nitidez:.1f}")

                st.markdown(f"**Descrição:** {record.descricao}")
                st.markdown(f"**Objetos/Elementos:** {record.objetos}")
                st.markdown(f"**Cores Predominantes:** {record.cores}")
                st.markdown(f"**Emoção Estimada:** {record.emocao}")
                st.markdown(f"**Idade Estimada:** {record.idade}")

                with st.expander("Ver JSON Completo de Saída"):
                    st.json(record.json_resultado)

            except Exception as e:
                st.error(f"Ocorreu um erro durante o processamento: {str(e)}")
                logger.error(f"Erro no módulo de interface de captura: {str(e)}")
            finally:
                db.close()