import streamlit.components.v1 as components
import os

_RELEASE = False

if not _RELEASE:
    _component = components.declare_component(
        "thuringia_story",
        url="http://localhost:5173",
    )
else:
    _build_dir = os.path.join(os.path.dirname(__file__), "../../dist")
    _component = components.declare_component("story_viewer", path=_build_dir)


def story_viewer(template, data=None, mode="view", key=None):
    return _component(
        template=template,
        data=data,
        mode=mode,
        key=key,
        default=None,
    )
