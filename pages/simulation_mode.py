import streamlit as st
from components import story_viewer
from shared import setup_page

setup_page()

st.markdown("""
    <style>
        .stMainBlockContainer { padding: 0; margin: 0; max-width: 100%; }
        .stAppHeader { display: none; }
        section[data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

if "data" not in st.session_state or st.session_state.data is None:
    st.switch_page("app.py")

# if st.button("← Back to upload"):
#     st.switch_page("app.py")

story_viewer(
    template="thuringia",
    data=st.session_state.data,
    mode="simulation",
)