import streamlit as st
import pandas as pd
from components import story_viewer
from shared import setup_page

DEFAULT_COLORS = ["#E14A2C", "#9DAEFF", "#EFD33F", "#007E4E"]

selected = st.session_state.get("selected_template", "thuringia")
selected_template_label = st.session_state.get("selected_template_label", "")

setup_page(
    show_top_bar=True,
    top_bar_links=[
        {"label": f"{selected_template_label}", "href": "/simulation_mode"},
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

if "arrow_colors" not in st.session_state:
    st.session_state.arrow_colors = DEFAULT_COLORS.copy()

print("columnLabelMap in session:", bool(st.session_state.get("columnLabelMap")))
print("keys sample:", list((st.session_state.get("columnLabelMap") or {}).items())[:5])

result = story_viewer(
    template=selected,
    data=st.session_state.data,
    columnLabelMap=st.session_state.get("columnLabelMap"),
    categoryColours=st.session_state.arrow_colors,
    mode="simulation",
    key="story",
)

if result and isinstance(result, dict) and result.get("action") == "open_data_editor":

    @st.dialog("CSV bearbeiten")
    def edit_csv_dialog():
        df = pd.DataFrame(st.session_state.data)

        edited_df = st.data_editor(
            df,
            width="stretch",
            num_rows="dynamic",
            key="csv_editor",
        )

        st.markdown(
            "<h3 style='margin-bottom: 8px;'>Change colours of categories:</h3>",
            unsafe_allow_html=True,
        )

        # 4 chips in one row
        c1, c2, c3, c4 = st.columns(4, gap="large")

        def color_chip(col, idx):
            with col:
                new = st.color_picker(
                    label="",
                    value=st.session_state.arrow_colors[idx],
                    key=f"arrow_color_{idx}",
                    label_visibility="collapsed",
                )
                st.session_state.arrow_colors[idx] = new

                # Hex label next to the picker
                st.markdown(
                    f"""
                    <div class="color-chip">
                    <span class="hex">{new}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        color_chip(c1, 0)
        color_chip(c2, 1)
        color_chip(c3, 2)
        color_chip(c4, 3)

        spacer, right = st.columns([8, 2])
        with right:
            if st.button("Speichern", use_container_width=True, key="csv_save_btn"):
                st.session_state.data = edited_df.to_dict(orient="records")
                st.rerun()

    edit_csv_dialog()
