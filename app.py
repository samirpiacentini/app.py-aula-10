import streamlit as st
from database.connection import init_db, engine
from utils.logger import logger

st.set_page_config(
    page_title="Visão Computacional - Dashboard",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega estilização CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

def check_db_status() -> bool:
    """Verifica resiliência da conexão com o banco Neon.tech."""
    return init_db()

def main():
    st.title("👁️ Plataforma de Visão Computacional em Tempo Real")
    st.markdown("---")

    # Status da Conexão na Sidebar
    st.sidebar.title("Navegação & Status")
    db_connected = check_db_status()

    if db_connected:
        st.sidebar.success("🟢 Conectado ao Neon.tech (PostgreSQL)")
    else:
        st.sidebar.error("🔴 Erro de conexão com o Banco de Dados")

    st.markdown("""
    ### Bem-vindo à plataforma de Visão Computacional!
    
    Esta aplicação permite capturar imagens via câmera do computador, processá-las em tempo real através de 
    algoritmos de **Visão Computacional (OpenCV)** e salvar os resultados de forma persistente.
    
    #### Funcionalidades Principais:
    - **📷 Captura e Análise:** Acesse a webcam, capture fotos e visualize o diagnóstico instantâneo.
    - **📜 Histórico:** Busque, filtre por data, visualize e exporte (CSV/JSON) análises passadas.
    - **📊 Dashboard:** Visualize dados consolidados e estatísticas das imagens processadas.
    
    Utilize o **menu lateral** para navegar entre os módulos.
    """)

    st.info("💡 **Dica DevOps:** Toda a estrutura está configurada para deploy automático no Render via GitHub!")

if __name__ == "__main__":
    main()