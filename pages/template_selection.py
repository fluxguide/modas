import streamlit as st
from st_clickable_images import clickable_images
from shared import setup_page
import html

# Debug
print(
    "Has data:",
    "data" in st.session_state,
    "len:",
    len(st.session_state.get("data", [])),
)

setup_page(
    show_top_bar=True,
    top_bar_links=[
        {"label": "Templates", "href": "/template_selection"},
        {"label": "About MoDaS", "href": "/about_modas"},
    ],
    active_page="/template_selection",
    top_bar_right_button={"label": "Reupload file", "href": "/"},
)

IMG_URL_BASE = "/app/static/img/Suite/Template_Previews"  # for clickable_images
IMG_FILE_BASE = "static/img/Suite/Template_Previews"  # for st.image local file read

templates = [
    {
        "key": "thuringia",
        "label": "Thuringia",
        "img_url": f"{IMG_URL_BASE}/Thuringia-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/Thuringia-Preview.png",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "suitable_for": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
    },
    {
        "key": "vrr",
        "label": "VRR",
        "img_url": f"{IMG_URL_BASE}/VRR-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/VRR-Preview.png",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "suitable_for": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
    },
    {
        "key": "dresden",
        "label": "Dresden",
        "img_url": f"{IMG_URL_BASE}/Dresden-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/Dresden-Preview.png",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "suitable_for": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
    },
    {
        "key": "story4",
        "label": "Story 4",
        "img_url": f"{IMG_URL_BASE}/Dortmund-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/Dortmund-Preview.png",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "suitable_for": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
    },
    {
        "key": "story5",
        "label": "Story 5",
        "img_url": f"{IMG_URL_BASE}/Ilmenau-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/Ilmenau-Preview.png",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "suitable_for": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
    },
]

uploaded_filename = html.escape(st.session_state.get("uploaded_filename", ""))

st.markdown(
    f"""
    <div class="template-page-instructions">
        <p>
            <span>{uploaded_filename}</span> has been uploaded successfully.
        </p>
        <h4>
            Click a template preview to view details and select the layout for your story simulation.
        </h4>
    </div>
    """,
    unsafe_allow_html=True,
)

clicked = clickable_images(
    [t["img_url"] for t in templates],
    titles=[t["label"] for t in templates],
    div_style={
        "display": "grid",
        "gridTemplateColumns": "repeat(3, 1fr)",
        "gap": "50px",
        "margin": "0 5vw",
    },
    img_style={
        "width": "100%",
        "height": "fit-content",
        "objectFit": "cover",
        "borderRadius": "12px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.14)",
        "cursor": "pointer",
    },
)

if clicked > -1:
    st.session_state.preview_template = templates[clicked]["key"]

template_by_key = {t["key"]: t for t in templates}
preview_key = st.session_state.get("preview_template")

if preview_key and preview_key in template_by_key:
    tpl = template_by_key[preview_key]

    @st.dialog(f"{tpl['label']} story")
    def template_dialog():
        left, right = st.columns([1.15, 1], gap="large")

        with left:
            st.image(tpl["img_file"], width="stretch")

        with right:
            st.markdown(
                f"""
                <div class="template-dialog-text">
                    <h3>About the original story</h3>
                    <p>{tpl["description"]}</p>
                    <h3>Suitable for</h3>
                    <p>{tpl["suitable_for"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Select this template",
                width="stretch",
                key="tpl_select",
            ):
                st.session_state.selected_template = tpl["key"]
                st.session_state.selected_template_label = tpl["label"]
                st.session_state.preview_template = None
                st.switch_page("pages/simulation_mode.py")

    template_dialog()

st.markdown("</div>", unsafe_allow_html=True)
