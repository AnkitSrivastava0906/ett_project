import streamlit as st
import pandas as pd
from visualization import show_basic_plots
from preprocessing import preprocess_data, auto_feature_engineer, analyze_dataset
from local_llm import ask_llm
from file_loader import load_dataset   # IMPORTANT

st.set_page_config(
    page_title="AI Data Assistant",
    layout="wide"
)

# Page state
if "page" not in st.session_state:
    st.session_state.page = "landing"


# ================= LANDING PAGE =================
def show_landing_page():
    st.title("🤖 AI Data Analyst")
    st.write("Upload your dataset to begin")

    file = st.file_uploader(
        "Upload dataset",
        type=["csv", "xlsx", "xls"]
    )

    if file:
        st.session_state.file = file

        if st.button("Start Analysis"):
            st.session_state.page = "dashboard"


# ================= DASHBOARD =================
def show_dashboard():
    st.title("📊 Data Analysis Dashboard")

    section = st.sidebar.radio(
        "Navigate",
        [
            "Auto Insights",
            "AI Recommendations",
            "Dataset Analysis",
            "EDA",
            "Chat"
        ]
    )

    file = st.session_state.file

    # 🔥 LOAD DATA (using your fixed loader)
    df = load_dataset(file)

    # 🔥 PROCESS
    df = preprocess_data(df)
    df, fe_actions = auto_feature_engineer(df)
    analysis = analyze_dataset(df)

    # ================= AUTO INSIGHTS =================
    if section == "Auto Insights":
        st.subheader("🤖 Auto Insights")

        with st.spinner("Generating insights..."):
            context = f"""
            Dataset summary:
            {analysis["dataset_summary"]}

            Columns:
            {analysis["columns"]}

            Warnings:
            {analysis["warnings"]}
            """

            insights = ask_llm(context)

        st.write(insights)

    # ================= AI RECOMMENDATIONS =================
    elif section == "AI Recommendations":
        st.subheader("🧠 AI Recommendations")

        with st.spinner("Generating recommendations..."):
            context = f"""
            Dataset summary:
            {analysis["dataset_summary"]}

            Columns:
            {analysis["columns"]}

            Warnings:
            {analysis["warnings"]}

            Suggested actions:
            {analysis["suggested_actions"]}
            """

            prompt = f"""
            You are a senior data scientist.

            Suggest:
            1. Data cleaning steps
            2. Feature engineering ideas
            3. Target variable
            4. ML models
            5. Improvements

            Data:
            {context}
            """

            recommendations = ask_llm(prompt)

        st.write(recommendations)

    # ================= EDA =================
    elif section == "EDA":
        st.subheader("📊 Exploratory Data Analysis")
        show_basic_plots(df)

    # ================= DATASET ANALYSIS =================
    elif section == "Dataset Analysis":
        st.subheader("📂 Dataset Overview")

        st.write("### Dataset Summary")
        st.json(analysis["dataset_summary"])

        if analysis["warnings"]:
            st.write("### ⚠ Warnings")
            for w in analysis["warnings"]:
                st.write("-", w)

        if analysis["suggested_actions"]:
            st.write("### 💡 Suggested Actions")
            for s in analysis["suggested_actions"]:
                st.write("-", s)

    # ================= CHAT =================
    elif section == "Chat":
        st.subheader("💬 Ask Questions")

        user_question = st.text_input("Ask anything about your data:")

        if user_question:
            with st.spinner("Thinking..."):
                context = f"""
                Dataset summary:
                {analysis["dataset_summary"]}

                Columns:
                {analysis["columns"]}
                """

                prompt = f"""
                Answer the question based on dataset:

                {context}

                Question:
                {user_question}
                """

                response = ask_llm(prompt)

            st.write(response)


# ================= ROUTER =================
if st.session_state.page == "landing":
    show_landing_page()
else:
    show_dashboard()


