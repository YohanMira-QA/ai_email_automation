import streamlit as st
import pandas as pd
import plotly.express as px
from ai_classifier import classify_email
from auto_responder import generate_response

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

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if username == "admin" and password == "1234":
            st.session_state["authenticated"] = True
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
st.write("Sube un archivo CSV con columna 'email_body'")

uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "email_body" not in df.columns:
        st.error("El archivo debe contener columna 'email_body'")
    else:
        categories = []
        responses = []

        with st.spinner("Procesando emails..."):
            for content in df["email_body"]:
                category = classify_email(content)
                response = generate_response(category)
                categories.append(category)
                responses.append(response)

        df["category"] = categories
        df["auto_response"] = responses

        st.success("Proceso completado ✅")

        # -----------------------
        # MÉTRICAS
        # -----------------------

        st.subheader("📊 Métricas Generales")

        total = len(df)
        leads = (df["category"] == "Lead").sum()
        support = (df["category"] == "Support").sum()
        invoices = (df["category"] == "Invoice").sum()
        spam = (df["category"] == "Spam").sum()

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Emails", total)
        col2.metric("Leads", leads)
        col3.metric("Support", support)
        col4.metric("Invoices", invoices)
        col5.metric("Spam", spam)

        # -----------------------
        # GRÁFICOS
        # -----------------------

        st.subheader("📈 Distribución por Categoría")

        fig = px.pie(
            df,
            names="category",
            title="Email Classification Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -----------------------
        # TABLA
        # -----------------------

        st.subheader("📋 Resultados Detallados")
        st.dataframe(df)

        # -----------------------
        # DESCARGA
        # -----------------------

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Descargar resultados",
            csv,
            "classified_emails.csv",
            "text/csv"
        )