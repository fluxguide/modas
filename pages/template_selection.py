import streamlit as st
from st_clickable_images import clickable_images
from shared import setup_page

st.write("Has data:", "data" in st.session_state, "len:", len(st.session_state.get("data", [])))

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
    ("story4", "Story 4", f"{IMG_BASE}/Thuringia-Preview.png"),
    ("vrr", "VRR", f"{IMG_BASE}/VRR-Preview.png"),
    ("story5", "Story 5", f"{IMG_BASE}/VRR-Preview.png"),
    ("dresden", "Dresden", f"{IMG_BASE}/Dresden-Preview.png"),
]


st.markdown(
    '<div class="template-grid"><h2>Choose the template for your story</h2>',
    unsafe_allow_html=True,
)

clicked = clickable_images(
    [t[2] for t in templates],
    titles=[t[1] for t in templates],
    div_style={
        "display": "grid",
        "gridTemplateColumns": "repeat(3, 1fr)",
        "gap": "30px",
    },
    img_style={
        "width": "100%",
        "height": "25vh",
        "objectFit": "cover",
        "borderRadius": "12px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.14)",
        "cursor": "pointer",
    },
)

if clicked > -1:
    st.session_state.selected_template = templates[clicked][0]
    st.session_state.selected_template_label = templates[clicked][1]

selected_key = st.session_state.get("selected_template", "")
selected_label = st.session_state.get("selected_template_label", "")

if selected_key:
    st.markdown(f"**Selected:** {selected_label}")
else:
    st.markdown("Click a template to select it.")

st.markdown("</div>", unsafe_allow_html=True)

if st.button(
    "Submit your choice", use_container_width=True, disabled=not bool(selected_key)
):
    st.switch_page("pages/simulation_mode.py")
