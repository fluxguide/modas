import streamlit as st
from components import story_viewer
from shared import setup_page

selected = st.session_state.get("selected_template", "thuringia")

setup_page(
    show_top_bar=True,
    top_bar_links=[
        {"label": f"{selected.title()} Story", "href": "/simulation_mode"},
    ],
    active_page="/simulation_mode",
    top_bar_right_button={"label": "Leave Simulation Mode", "href": "/"},
)

data = st.session_state.get("data")
if not data:
    st.warning("No uploaded data found in this session. Please upload your CSV first.")
    if st.button("Go to upload", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

story_viewer(template=selected, data=data, mode="simulation")
