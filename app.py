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
            <h1>Mobility Data Story Suite (MoDaS)</h1>
            <p>How can mobility data be communicated in an understandable and effective way? As a technology partner for the mfund project MoDaS, we developed a platform that translates abstract mobility data into comprehensible storytelling formats.</p>
            <p>Together with our research partner TU Ilmenau, we developed a ‘Mobility Data Story Suite’ that visualises traffic data through digital storytelling. The target group is mobility planners, political decision-makers and citizens. The Mobility Data Story Suite makes complex data interactively available using innovative storytelling methods, thereby improving the efficiency of mobility planning processes.</p>
            <h3>Ready to create your own story?</h3>
            <ol>
                <li><p>Upload your data file and submit it</p></li>
                <li><p>Select one of the available templates</p></li>
                <li><p>Proceed to the simulation mode, and make some changes in the template if needed</p></li>
            </ol>
        </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload CSV file", type="csv", label_visibility="collapsed"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if st.button("Submit", width="stretch"):
            st.session_state.data = df.to_dict(orient="records")
            st.switch_page("pages/template_selection.py")

    st.markdown(
        f"""
        <p class="explore-link">
            Do not have any data yet? 
            <a href="https://mobilithek.info/">Explore Mobilithek</a>
        </p>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div class="right-container" style="background-image: url(data:image/svg+xml;base64,{b64})"></div>',
        unsafe_allow_html=True,
    )
