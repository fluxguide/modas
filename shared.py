import streamlit as st


def top_bar(links=None, active=None, reupload_button=True):
    if links is None:
        links = [
            {"label": "Templates", "href": "/template_selection"},
            {"label": "About MoDaS", "href": "/about_modas"},
        ]

    links_html = ""
    for link in links:
        href = "#" if link["href"] == active else link["href"]
        cls = "active" if link["href"] == active else ""
        links_html += f'<a href="{href}" class="top-bar-link {cls}">{link["label"]}</a>'

    right_html = ""
    if reupload_button:
        right_html = f'<a href="{reupload_button["href"]}" class="top-bar-action">{reupload_button["label"]}</a>'

    st.markdown(
        f"""
        <div class="top-bar">
            <div class="top-bar-left">{links_html}</div>
            <div class="top-bar-right">{right_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def setup_page(
    show_top_bar=True, top_bar_links=None, active_page=None, top_bar_right_button=None
):
    st.set_page_config(layout="wide")
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    if show_top_bar:
        top_bar(top_bar_links, active_page, reupload_button=top_bar_right_button)
