import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
from dotenv import load_dotenv
from core.ai_classifier import classify_email
from core.auto_responder import generate_response
from utils.dashboard_utils import prepare_download

# -----------------------
# CARGAR VARIABLES .ENV
# -----------------------
load_dotenv()


APP_USERNAME = os.getenv("APP_USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# -----------------------
# CONFIGURACIÓN GENERAL
# -----------------------
st.set_page_config(
    page_title="AI Email Automation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# LOGIN SIMPLE
# -----------------------
def login():
    st.title("🔐 Business Automation Login")

    user_input = st.text_input("Usuario")
    password_input = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user_input == APP_USERNAME and password_input == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Login exitoso ✅")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# -----------------------
# DASHBOARD PRINCIPAL
# -----------------------

st.title("📧 AI Email Automation Dashboard")
st.write("Sube un archivo CSV con columna **email_body**")

uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    if "email_body" not in df.columns:
        st.error("El archivo debe contener la columna 'email_body'")
        st.stop()

    # -----------------------
    # PROCESAMIENTO
    # -----------------------

    with st.spinner("Procesando emails..."):
        df["category"] = df["email_body"].apply(classify_email)
        df["auto_response"] = df["category"].apply(generate_response)

    st.success("Proceso completado ✅")

    # -----------------------
    # MÉTRICAS DINÁMICAS
    # -----------------------

    st.subheader("📊 Métricas Generales")

    total = len(df)
    category_counts = df["category"].value_counts()

    cols = st.columns(len(category_counts) + 1)

    cols[0].metric("Total Emails", total)

    for i, (category, count) in enumerate(category_counts.items()):
        cols[i + 1].metric(category, count)

    # -----------------------
    # GRÁFICO
    # -----------------------

    st.subheader("📈 Distribución por Categoría")

    fig = px.pie(
        df,
        names="category",
        title="Email Classification Distribution",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------
    # TABLA
    # -----------------------

    st.subheader("📋 Resultados Detallados")
    st.dataframe(df, use_container_width=True)

    # -----------------------
    # DESCARGA COMPATIBLE EXCEL
    # -----------------------

    clean_df = prepare_download(df)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        clean_df.to_excel(writer, index=False, sheet_name="Resultados")

    st.download_button(
    label="⬇ Descargar resultados en Excel",
    data=output.getvalue(),
    file_name="classified_emails.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)