import streamlit as st
import plotly.express as px

def show_basic_plots(df):
    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    # Bar chart
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        fig = px.bar(
            df,
            x=categorical_cols[0],
            y=numeric_cols[0],
            title=f"{numeric_cols[0]} vs {categorical_cols[0]}"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough categorical or numerical columns for bar chart.")

    # Correlation heatmap
    valid_numeric_cols = [col for col in numeric_cols if df[col].nunique() > 1]

    if len(valid_numeric_cols) > 1:
        corr = df[valid_numeric_cols].corr()
        fig = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Heatmap"
        )
        st.plotly_chart(fig, use_container_width=True)
