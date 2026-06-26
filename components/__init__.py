import streamlit.components.v1 as components
import os

# Release mode is driven by the STREAMLIT_RELEASE env var (set in the Docker
# image). In dev it is unset, so the component loads from the Vite dev server.
_RELEASE = os.environ.get("STREAMLIT_RELEASE", "").lower() in ("1", "true", "yes")

if not _RELEASE:
    _component = components.declare_component(
        "story_viewer",
        url="http://localhost:5173",
    )
else:
    _build_dir = os.path.join(os.path.dirname(__file__), "../dist")
    _component = components.declare_component("story_viewer", path=_build_dir)


def story_viewer(
    template, data=None, columnLabelMap=None, categoryColours=None, mode="view", height=900, key=None, selectedCity=None
):
    return _component(
        template=template,
        data=data,
        columnLabelMap=columnLabelMap,
        categoryColours=categoryColours,
        mode=mode,
        key=key,
        default=None,
        height=height,
        selectedCity=selectedCity,
    )
