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
    top_bar_right_button={"label": "Neustadt", "href": "/"},
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

        st.markdown("<h3>Change colours of categories:</h3>", unsafe_allow_html=True)

        st.markdown(
            """
                <style>
                div[data-testid="stLayoutWrapper"]>.stVerticalBlock {
                    gap: 0.5rem !important;
                }
                
                div[data-testid="stLayoutWrapper"]>.stHorizontalBlock {
                    gap: 1rem !important;
                    margin-bottom: 3rem !important;
                }
                
                div[data-testid="stDialog"] div.stButton {
                    margin-right: 0rem !important;
                    margin-left: auto !important;
                }
                
                div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
                    flex-flow: row !important;
                    justify-content: flex-start;
                    gap: 25%;
                    background: #ffffff;
                    border-radius: 16px;
                    border: 1.5px solid #e8e8e8;
                    padding: 10px 16px;
                    width: fit-content !important;
                }
                
                div.stButton>button {
                    padding: 12px 32px;
                }

                /* Hide the label */
                div[data-testid="stColorPicker"] label {
                    display: none !important;
                }

                /* Remove default card styling from the picker wrapper */
                div[data-testid="stColorPicker"] > div {
                    background: transparent !important;
                    border-radius: 0 !important;
                    padding: 0 !important;
                    box-shadow: none !important;
                }
                
                div[data-testid="stColorPicker"]>div>div {
                    display: flex;
                    align-items: center;
                    gap: 14px;
                }

                div[data-testid="stColorPicker"] {
                    flex-shrink: 0;
                }

                .hex-label {
                    font-size: 16px;
                    font-weight: 400;
                    color: #222222;
                    white-space: nowrap;
                    line-height: 1;
                    margin-right: 15px;
                }

                [data-testid="stMarkdownContainer"] {
                    display: flex;
                    align-items: center;
                }
                
                [data-testid="stMarkdownContainer"] > p {
                    margin: 0;
                }
                </style>
                """,
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4, gap="medium")

        def color_chip(col, id):
            with col:
                new = st.color_picker(
                    label="color",
                    value=st.session_state.arrow_colors[id],
                    key=f"arrow_color_{id}",
                    label_visibility="collapsed",
                )
                st.session_state.arrow_colors[id] = new
                st.markdown(
                    f'<span class="hex-label">{new}</span>',
                    unsafe_allow_html=True,
                )

        color_chip(c1, 0)
        color_chip(c2, 1)
        color_chip(c3, 2)
        color_chip(c4, 3)

        if st.button("Speichern", width="stretch", key="csv_save_btn"):
            st.session_state.data = edited_df.to_dict(orient="records")
            st.session_state["story"] = None
            st.rerun()

    edit_csv_dialog()
