import streamlit as st
import pandas as pd
import base64
from components import story_viewer

# MARK: Base Setup
st.set_page_config(layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Track which screen we're on
if "screen" not in st.session_state:
    st.session_state.screen = "upload"
if "data" not in st.session_state:
    st.session_state.data = None


# MARK: Screen 1 — Upload
if st.session_state.screen == "upload":
    with open("assets/img/Suite/modas-side-img.svg", "r") as f:
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
            st.dataframe(df.head(), width="stretch")

            if st.button("Submit", width="stretch"):
                st.session_state.data = df.to_dict(orient="records")
                st.session_state.screen = "story"
                st.rerun()

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


# MARK: Screen 2 — Story
elif st.session_state.screen == "story":
    if st.button("← Back to upload"):
        st.session_state.screen = "upload"
        st.session_state.data = None
        st.rerun()

    story_viewer(
        template="thuringia",
        data=st.session_state.data,
        mode="simulation",
    )

# MARK: Future
# Retrieving table data --> will need later
# uploaded_files = st.file_uploader("Upload data", accept_multiple_files=True, type="csv")
# for uploaded_file in uploaded_files:
#     df = pd.read_csv(uploaded_file)
#     edited_df = st.data_editor(df)
