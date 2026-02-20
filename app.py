import streamlit as st
import pandas as pd
import base64
from shared import setup_page

setup_page(show_top_bar=False)

with open("static/img/Suite/modas-side-img.svg", "r") as f:
    svg_content = f.read()
b64 = base64.b64encode(svg_content.encode()).decode()

col1, col2 = st.columns(2, gap="small")

with col1:
    primary = st.get_option("theme.primaryColor")

    st.markdown(
        """
        <div class="left-container">
            <p>A brief Explanation here</p>
            <p>Before you start please watch the video with instructions</p>
            <h2>Upload File</h2>
            <p>Select and upload the file of your choice</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload CSV file", type="csv", label_visibility="collapsed"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(), width='stretch')

        if st.button("Submit", width='stretch'):
            st.session_state.data = df.to_dict(orient="records")
            st.switch_page("pages/template_selection.py")

    st.markdown(
        f"""
        <p class="explore-link">
            Do not have any data yet? 
            <span style="color:{primary}; font-weight:bold">Explore Mobilithek</span>
        </p>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div class="right-container" style="background-image: url(data:image/svg+xml;base64,{b64})"></div>',
        unsafe_allow_html=True,
    )
