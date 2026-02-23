import streamlit as st
from st_clickable_images import clickable_images
from shared import setup_page

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

IMG_BASE = "/app/static/img/Suite/Template_Previews"

templates = [
    ("thuringia", "Thuringia", f"{IMG_BASE}/Thuringia-Preview.png"),
    ("vrr", "VRR", f"{IMG_BASE}/VRR-Preview.png"),
    ("dresden", "Dresden", f"{IMG_BASE}/Dresden-Preview.png"),
    ("story4", "Story 4", f"{IMG_BASE}/Thuringia-Preview.png"),
    ("story5", "Story 5", f"{IMG_BASE}/VRR-Preview.png"),
]


st.markdown(
    '<div class="template-page-title"><h2>Choose the template for your story</h2>',
    unsafe_allow_html=True,
)

clicked = clickable_images(
    [t[2] for t in templates],
    titles=[t[1] for t in templates],
    div_style={
        "display": "grid",
        "gridTemplateColumns": "repeat(3, 1fr)",
        "gap": "30px",
        "margin": "0 70px",
    },
    img_style={
        "width": "90%",
        "height": "fit-content",
        "objectFit": "cover",
        "borderRadius": "12px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.14)",
        "cursor": "pointer",
    },
)

if clicked > -1:
    st.session_state.selected_template = templates[clicked][0]
    st.session_state.selected_template_label = templates[clicked][1]

st.markdown("</div>", unsafe_allow_html=True)

selected_key = st.session_state.get("selected_template", "")
selected_label = st.session_state.get("selected_template_label", "")

st.markdown('<div class="submit-tmpl-btn"></div>', unsafe_allow_html=True)

if st.button("Submit your choice", disabled=not bool(selected_key), key=selected_key):
    st.switch_page("pages/simulation_mode.py")
