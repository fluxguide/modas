import streamlit.components.v1 as components
import os

_RELEASE = False  # set True when using built dist

if not _RELEASE:
    _component = components.declare_component(
        "vue_color_picker",
        url="http://localhost:5173",  # Vite dev server
    )
else:
    _build_dir = os.path.join(os.path.dirname(__file__), "frontend/dist")
    _component = components.declare_component("vue_color_picker", path=_build_dir)


def vue_color_picker(label="Pick a color", default="#494995", key=None):
    return _component(label=label, default=default, key=key)