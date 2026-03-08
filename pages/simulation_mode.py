import streamlit as st
import pandas as pd
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

result = story_viewer(
    template=selected,
    data=st.session_state.data,
    columnLabelMap=st.session_state.get("columnLabelMap"),
    mode="simulation",
    key="story",
)

if result and isinstance(result, dict) and result.get("action") == "open_data_editor":

    @st.dialog("CSV bearbeiten")
    def edit_csv_dialog():
        df = pd.DataFrame(st.session_state.data)

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="csv_editor",
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Abbrechen", use_container_width=True):
                st.rerun()
        with c2:
            if st.button("Speichern", use_container_width=True):
                st.session_state.data = edited_df.to_dict(orient="records")
                st.rerun()

    edit_csv_dialog()
