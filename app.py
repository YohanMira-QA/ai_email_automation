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
# LOAD ENV VARIABLES
# -----------------------
load_dotenv()

APP_USERNAME = os.getenv("USERNAME")
APP_PASSWORD = os.getenv("PASSWORD")

# -----------------------
# GENERAL CONFIGURATION
# -----------------------
st.set_page_config(
    page_title="AI Email Automation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# SIMPLE LOGIN
# -----------------------
def login():
    st.title("🔐 Business Automation Login")

    user_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        if user_input == APP_USERNAME and password_input == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()
# -----------------------
# SIDEBAR MENU
# -----------------------

with st.sidebar:
    st.title("⚙️ Menu")
    
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

# -----------------------
# MAIN DASHBOARD
# -----------------------

st.title("📧 AI Email Automation Dashboard")
st.write("Upload a CSV file containing the **email_body** column.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:

    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8", sep=",", quotechar='"')
    except Exception:
        try:
            df = pd.read_csv(uploaded_file, encoding="latin-1")
        except Exception:
            st.error("Unable to read the file. Please upload a valid CSV file.")
            st.stop()

    if "email_body" not in df.columns:
        st.error("The file must contain a column named 'email_body'")
        st.stop()

    # -----------------------
# PROCESSING
# -----------------------

# Clean data BEFORE processing
    df = df.dropna(subset=["email_body"]).copy()
    df["email_body"] = df["email_body"].astype(str)

    progress_bar = st.progress(0)
    status_text = st.empty()

    categories = []
    responses = []

    total_rows = len(df)

    for i in range(total_rows):
        email = df.iloc[i]["email_body"]

        category = classify_email(email)
        response = generate_response(category)

        categories.append(category)
        responses.append(response)

        progress = int((i + 1) / total_rows * 100)
        progress_bar.progress(progress)
        status_text.text(f"Processing email {i+1} of {total_rows}...")

    df["category"] = categories
    df["auto_response"] = responses

    progress_bar.empty()
    status_text.empty()

    st.success("Processing completed successfully ✅")
    # -----------------------
    # DYNAMIC METRICS
    # -----------------------

    st.subheader("📊 Overview Metrics")

    total = len(df)
    category_counts = df["category"].value_counts()

    cols = st.columns(len(category_counts) + 1)

    cols[0].metric("Total Emails", total)

    for i, (category, count) in enumerate(category_counts.items()):
        cols[i + 1].metric(category, count)

    # -----------------------
    # CHART
    # -----------------------

    st.subheader("📈 Category Distribution")

    fig = px.pie(
        df,
        names="category",
        title="Email Classification Distribution",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------
    # DATA TABLE
    # -----------------------

    st.subheader("📋 Detailed Results")
    st.dataframe(df, use_container_width=True)

    # -----------------------
    # EXCEL DOWNLOAD
    # -----------------------

    clean_df = prepare_download(df)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        clean_df.to_excel(writer, index=False, sheet_name="Results")

    st.download_button(
        label="⬇ Download Results (Excel)",
        data=output.getvalue(),
        file_name="classified_emails.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )