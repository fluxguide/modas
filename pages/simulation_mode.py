import streamlit as st
from components import story_viewer
from shared import setup_page

selected = st.session_state.get("selected_template", "thuringia")
selected_template_label = st.session_state.get("selected_template_label", "")

setup_page(
    show_top_bar=True,
    top_bar_links=[
        {"label": f"{selected_template_label.title()}", "href": "/simulation_mode"},
    ],
    active_page="/simulation_mode",
    top_bar_right_button={"label": "Datei ändern", "href": "/"},
)

data = st.session_state.get("data")
if not data:
    st.warning("No uploaded data found in this session. Please reupload your file.")
    if st.button("Go to upload", width="stretch"):
        st.switch_page("app.py")
    st.stop()
    
print("columnLabelMap in session:", bool(st.session_state.get("columnLabelMap")))
print("keys sample:", list((st.session_state.get("columnLabelMap") or {}).items())[:5])

story_viewer(
    template=selected,
    data=st.session_state.data,
    columnLabelMap=st.session_state.get("columnLabelMap"),
    mode="simulation",
)
