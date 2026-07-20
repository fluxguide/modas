import streamlit as st
import pandas as pd
from components import story_viewer
from shared import setup_page
import base64
import json
import os

STORY_COLOURS = {
    "thuringia": {
        0: ["#E14A2C", "#9DAEFF", "#EFD33F", "#007E4E"],
        1: ["#E14A2C", "#9DAEFF", "#EFD33F", "#007E4E"],
        2: ["#E14A2C", "#9DAEFF", "#EFD33F", "#007E4E"],
    },
    "vrr": {
        1: ["#001C0C", "#004F22", "#43A86B"],
        2: [
            "#001C0C",
        ],
        3: [
            "#52AE32",
            "#63BEDD",
        ],
    },
    "dresden": {
        1: [""],
    },
    "story4": {},
}

CHART_COLUMNS_BY_TEMPLATE = {
    "thuringia": {
        0: {"townhall_name", "townhall_city", "stops_within_100m"},
        1: {"townhall_name", "townhall_city", "stops_within_200m"},
        2: {"townhall_name", "townhall_city", "stops_within_300m"},
    },
    "vrr": {
        1: {"category", "chart number", "year1", "year2", "year3"},
        2: {"category", "chart number", "year1", "year2", "year3"},
        3: {"category", "percentage"},
    },
    "dresden": {
        0: {""},
    },
    "story4": {},
}

CITIES = [
    "Berlin",
    "Cologne",
    "Dortmund",
    "Dresden",
    "Dusseldorf",
    "Frankfurt",
    "Hamburg",
    "Leipzig",
    "Munich",
    "Stuttgart",
]

_REGIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "regions.json")
with open(_REGIONS_PATH, encoding="utf-8") as _f:
    _REGIONS = json.load(_f)

REGIONS = list(_REGIONS.keys())
REGION_BOUNDS = {region: cfg["bounds"] for region, cfg in _REGIONS.items()}
REGION_MAP_FILES = {region: cfg["map"] for region, cfg in _REGIONS.items()}

def detect_data_region(data, threshold=0.7):
    coords = []
    for row in data or []:
        try:
            lat = float(row.get("townhall_latitude"))
            lon = float(row.get("townhall_longitude"))
        except (TypeError, ValueError):
            continue
        if lat == 0 and lon == 0:
            continue
        coords.append((lon, lat))

    if not coords:
        return None

    total = len(coords)
    best = None
    for region, (west, south, east, north) in REGION_BOUNDS.items():
        inside = sum(
            1 for lon, lat in coords if west <= lon <= east and south <= lat <= north
        )
        if inside / total < threshold:
            continue
        area = (east - west) * (north - south)
        if best is None or area < best[0]:
            best = (area, region)

    return best[1] if best else None


def render_region_map_preview(region):
    filename = REGION_MAP_FILES.get(region)
    if not filename:
        st.warning(f"Keine Karte für {region} gefunden.")
        return

    path = f"static/img/Thuringia/maps/{filename}"
    mime = "image/svg+xml" if filename.lower().endswith(".svg") else "image/png"

    try:
        with open(path, "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        st.warning(f"Keine Karte für {region} gefunden.")
        return

    region_b64 = base64.b64encode(raw).decode()

    st.markdown(
        f"""
        <div style="
            border: 1.5px solid #e8e8e8;
            border-radius: 16px;
            padding: 16px;
            margin-top: 16px;
            margin-bottom: 24px;
            background: white;
            text-align: center;
        ">
            <img
                src="data:{mime};base64,{region_b64}"
                style="width: 100%; max-height: 360px; object-fit: contain; display: block;"
            />
            <p style="font-size: 16px; font-weight: 600; margin-top: 12px;">
                {region}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


selected = st.session_state.get("selected_template", "")
selected_template_label = st.session_state.get("selected_template_label", "")
selected_map_city = st.session_state.get("selected_map_city", "Dresden")

data = st.session_state.get("data")
if not data:
    st.warning(
        "In dieser Sitzung wurden keine hochgeladenen Daten gefunden. Bitte laden Sie Ihre Datei erneut hoch."
    )
    if st.button("Zum Upload", width="stretch"):
        st.switch_page("app.py")
    st.stop()

if selected == "thuringia" and "selected_map_region" not in st.session_state:
    st.session_state.selected_map_region = detect_data_region(data) or "Thüringen"

selected_map_region = st.session_state.get("selected_map_region", "Thüringen")

setup_page(
    show_top_bar=True,
    top_bar_links=[
        {"label": f"{selected_template_label}", "href": "/simulation_mode"},
    ],
    active_page="/simulation_mode",
    top_bar_right_button={"label": "Neustart", "href": "/"},
)


def get_story_colors(template):
    return STORY_COLOURS.get(template)


colours = get_story_colors(selected)

if "category_colors" not in st.session_state:
    st.session_state.category_colors = colours.copy()

if not isinstance(selected_map_city, str) or selected_map_city not in CITIES:
    selected_map_city = "Dresden"
    st.session_state.selected_map_city = "Dresden"

if not isinstance(selected_map_region, str) or selected_map_region not in REGIONS:
    selected_map_region = "Thüringen"
    st.session_state.selected_map_region = "Thüringen"

if selected == "thuringia":
    result = story_viewer(
        template=selected,
        data=st.session_state.data,
        columnLabelMap=st.session_state.get("columnLabelMap"),
        categoryColours=st.session_state.category_colors,
        mode="simulation",
        key="story",
        selectedRegion=selected_map_region,
    )
elif selected == "story4":
    result = story_viewer(
        template=selected,
        data=st.session_state.data,
        columnLabelMap=st.session_state.get("columnLabelMap"),
        categoryColours=st.session_state.category_colors,
        mode="simulation",
        key="story",
    )
else:
    result = story_viewer(
        template=selected,
        data=st.session_state.data,
        columnLabelMap=st.session_state.get("columnLabelMap"),
        categoryColours=st.session_state.category_colors,
        mode="simulation",
        key="story",
        selectedCity=selected_map_city,
    )

if result and isinstance(result, dict) and result.get("action") == "open_data_editor":

    @st.dialog("CSV bearbeiten")
    def edit_csv_dialog(template, current_range=None, chart_number=None):
        df = pd.DataFrame(st.session_state.data)

        template_columns = CHART_COLUMNS_BY_TEMPLATE.get(template, {})
        chart_key = current_range if current_range is not None else chart_number
        chart_columns = template_columns.get(chart_key, set())

        column_config = {
            col: st.column_config.Column(label=f"◆ {col}")
            for col in df.columns
            if col in chart_columns
        }
        print(
            column_config,
            f"\nColumns in editor: {list(column_config.keys())}, expected: {chart_columns}",
        )

        edited_df = st.data_editor(
            df,
            width="stretch",
            num_rows="dynamic",
            key="csv_editor",
            column_config=column_config,
        )

        st.markdown(
            '<p style="font-size:12px; color:#666; margin: 0px 0px 10px auto">◆ im Diagramm verwendete Spalten</p>',
            unsafe_allow_html=True,
        )

        st.markdown("<h3>Farben der Kategorien ändern:</h3>", unsafe_allow_html=True)

        st.markdown(
            """
                <style>
                div[data-testid="stLayoutWrapper"]>.stVerticalBlock {
                    gap: 0rem !important;
                }
                
                div[data-testid="stLayoutWrapper"]>.stHorizontalBlock {
                    gap: 1rem !important;
                    margin-bottom: 3rem !important;
                }
                
                div[data-testid="stLayoutWrapper"]>.stHorizontalBlock>* {
                    width: 100% !important;
                    flex: 0;
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

        def color_chip(col, chart_number, id):
            with col:
                new = st.color_picker(
                    label="color",
                    value=st.session_state.category_colors[chart_number][id],
                    key=f"category_color_{chart_number}_{id}",
                    label_visibility="collapsed",
                )
                st.session_state.category_colors[chart_number][id] = new
                st.markdown(
                    f'<span class="hex-label">{new}</span>',
                    unsafe_allow_html=True,
                )

        colors_to_show = []
        if chart_key is not None:
            colors_to_show = st.session_state.category_colors.get(chart_key, []) or []

        if colors_to_show:
            cols = st.columns(len(colors_to_show), gap="medium")
            for i, col in enumerate(cols):
                color_chip(col, chart_key, i)
        else:
            st.caption("Keine Kategoriefarben für dieses Diagramm definiert.")

        if st.button("Speichern", width="stretch", key="csv_save_btn"):
            st.session_state.data = edited_df.to_dict(orient="records")
            st.session_state["story"] = None
            st.rerun()


if result and isinstance(result, dict) and result.get("action") == "open_data_editor":
    edit_csv_dialog(selected, result.get("currentRange"), result.get("chartNumber"))

open_map_editor = (
    result and isinstance(result, dict) and result.get("action") == "open_map_editor"
) or st.session_state.pop("force_open_map_editor", False)

if open_map_editor:

    @st.dialog("Karte bearbeiten")
    def edit_map_dialog():
        current_city = st.session_state.get("selected_map_city", "Dresden")

        if current_city not in CITIES:
            current_city = "Dresden"

        st.markdown(
            """
                <style>
                
                div[data-testid="stSelectbox"] > div > div {
                    background-color: white !important;
                    cursor: pointer !important;
                }

                div[data-testid="stSelectbox"] > div:focus-within {
                    border-color: #010080 !important;
                    box-shadow: none !important;
                }

                div[data-testid="stSelectbox"] label {
                    font-size: 14px;
                    color: #222222;
                }
                </style>
            """,
            unsafe_allow_html=True,
        )

        selected_city = st.selectbox(
            "Stadt auswählen",
            CITIES,
            index=CITIES.index(current_city),
            key="draft_selected_map_city",
        )

        try:
            with open(f"static/img/Dresden/{selected_city}Map.svg", "r") as f:
                svg_preview = f.read()

            svg_b64 = base64.b64encode(svg_preview.encode()).decode()

            st.markdown(
                f"""
                <div style="
                    border: 1.5px solid #e8e8e8;
                    border-radius: 16px;
                    padding: 16px;
                    margin-top: 16px;
                    margin-bottom: 24px;
                    background: white;
                    text-align: center;
                ">
                    <img 
                        src="data:image/svg+xml;base64,{svg_b64}" 
                        style="width: 100%; max-height: 360px; object-fit: contain; display: block;"
                    />
                    <p style="font-size: 16px; font-weight: 600; margin-top: 12px;">
                        {selected_city}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        except FileNotFoundError:
            st.warning(f"Keine SVG für {selected_city} gefunden.")

        col1, col2 = st.columns([5, 1])

        with col2:
            if st.button("Auswahl speichern", width="stretch", key="map_save_btn"):
                st.session_state.selected_map_city = selected_city
                st.session_state["story"] = None

                if "draft_selected_map_city" in st.session_state:
                    del st.session_state["draft_selected_map_city"]

                st.rerun()

    @st.dialog("Karte bearbeiten")
    def edit_region_map_dialog():
        current_region = st.session_state.get("selected_map_region", "Thüringen")

        if current_region not in REGIONS:
            current_region = "Thüringen"

        st.markdown(
            """
                <style>

                div[data-testid="stSelectbox"] > div > div {
                    background-color: white !important;
                    cursor: pointer !important;
                }

                div[data-testid="stSelectbox"] > div:focus-within {
                    border-color: #010080 !important;
                    box-shadow: none !important;
                }

                div[data-testid="stSelectbox"] label {
                    font-size: 14px;
                    color: #222222;
                }
                </style>
            """,
            unsafe_allow_html=True,
        )

        selected_region = st.selectbox(
            "Region auswählen",
            REGIONS,
            index=REGIONS.index(current_region),
            key="draft_selected_map_region",
        )

        render_region_map_preview(selected_region)

        col1, col2 = st.columns([5, 1])

        with col2:
            if st.button("Auswahl speichern", width="stretch", key="map_save_btn"):
                st.session_state.selected_map_region = selected_region
                st.session_state["story"] = None
                st.session_state.map_selection_touched = True
                st.session_state.map_mismatch_ack = None

                if "draft_selected_map_region" in st.session_state:
                    del st.session_state["draft_selected_map_region"]

                st.rerun()

    if selected == "thuringia":
        edit_region_map_dialog()
    else:
        edit_map_dialog()

if (
    selected == "thuringia"
    and not open_map_editor
    and st.session_state.get("map_selection_touched")
):
    proper_region = detect_data_region(st.session_state.data)

    if (
        proper_region
        and proper_region != selected_map_region
        and st.session_state.get("map_mismatch_ack") != selected_map_region
    ):

        @st.dialog("Karte passt nicht zu den Daten")
        def region_mismatch_dialog():
            st.markdown(
                f"Diese Karte passt nicht zu Ihren Daten, da Ihre Daten für "
                f"**{proper_region}** sind."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Mit dieser Karte fortfahren",
                    width="stretch",
                    key="mismatch_continue_btn",
                ):
                    st.session_state.map_mismatch_ack = selected_map_region
                    st.rerun()

            with col2:
                if st.button(
                    "Karte ändern",
                    width="stretch",
                    key="mismatch_change_btn",
                ):
                    st.session_state.map_mismatch_ack = None
                    st.session_state.force_open_map_editor = True
                    st.rerun()

        region_mismatch_dialog()
