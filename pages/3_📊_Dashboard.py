import streamlit as st
import pandas as pd
from database.connection import SessionLocal
from controllers.main_controller import MainController

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard e Métricas de Qualidade")
st.markdown("---")

db = SessionLocal()
try:
    controller = MainController()
    records = controller.fetch_history(db)
finally:
    db.close()

if not records:
    st.warning("Sem dados suficientes no banco de dados para gerar gráficos.")
else:
    data = [r.to_dict() for r in records]
    df = pd.DataFrame(data)
    df["created_at"] = pd.to_datetime(df["created_at"])

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total de Capturas", len(df))
    kpi2.metric("Total de Rostos Detectados", int(df["rostos"].sum()))
    kpi3.metric("Luminosidade Média", f"{df['luminosidade'].mean():.1f}")
    kpi4.metric("Nitidez Média", f"{df['nitidez'].mean():.1f}")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Capturas ao Longo do Tempo")
        df_time = df.set_index("created_at").resample("D").size().reset_index(name="quantidade")
        st.line_chart(df_time, x="created_at", y="quantidade")

    with col_chart2:
        st.subheader("Distribuição da Detecção de Rostos")
        st.bar_chart(df["rostos"].value_counts())