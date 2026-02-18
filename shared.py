import streamlit as st


def top_bar():
    st.markdown(
        """
        <div class="top-bar">
            <a href="/">Home</a>
            <a href="/template_selection">Templates</a>
            <a href="/simulation_mode">Simulation</a>
        </div>
    """,
        unsafe_allow_html=True,
    )


def setup_page(show_top_bar=True):
    st.set_page_config(layout="wide")
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    if show_top_bar:
        top_bar()
