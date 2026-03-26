import streamlit as st
import pandas as pd
import re
import base64
from shared import setup_page

setup_page(show_top_bar=False)

languages = {
    "de": {
        "button": "Dateien durchsuchen",
        "instructions": "Datei hierher ziehen und ablegen",
        "limits": "Maximal 200MB pro Datei",
    },
    # "en": {
    #     "button": "Browse files",
    #     "instructions": "Drag and drop files here",
    #     "limits": "Maximum 200MB per file"
    # }
}

with open("./style.css") as f:
    css_content = f.read()

st.markdown(
    f"""
    <style>
    :root {{
        --label-button: "{languages['de']['button']}";
        --label-instructions: "{languages['de']['instructions']}";
        --label-limits: "{languages['de']['limits']}";
    }}
    {css_content}
    </style>
""",
    unsafe_allow_html=True,
)

with open("static/img/Suite/modas-side-img.svg", "r") as f:
    svg_content = f.read()
b64 = base64.b64encode(svg_content.encode()).decode()


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.strip().lower()).strip("_")


col1, col2 = st.columns(2, gap="small")

with col1:
    primary = st.get_option("theme.primaryColor")

    st.markdown(
        """
        <div class="left-container">
            <h1>Mobility Data Story-Suite (MoDaS)</h1>
            <h4>Von Mobilitätsdaten zum Storytelling</h4>
            <p>Als Technologiepartner im mfund-Projekt MoDaS haben wir eine Plattform entwickelt, die abstrakte Mobilitätsdaten in leicht verständliche Storytelling-Formate überträgt. In enger Zusammenarbeit mit unserem Forschungspartner TU Ilmenau entstand die „Mobility Data Story Suite“, ein innovatives Tool, das Verkehrsdaten durch digitales Storytelling visualisiert. Zielgruppe sind Mobilitätsplanende, politische Entscheidungstragende und Bürger*innen gleichermaßen.</p>
            <p>Die Mobility Data Story Suite macht komplexe Daten interaktiv erfahrbar und nutzt moderne Storytelling-Methoden, um Entscheidungsprozesse zu unterstützen. So trägt sie dazu bei, Mobilitätsplanung effizienter, nachvollziehbarer und transparenter zu gestalten.</p>
            <h3>Sind Sie bereit, Ihre eigene Geschichte zu erstellen?</h3>
            <ol>
                <li><p>Laden Sie Ihre Datei mit den Mobilitätsdaten hoch und senden Sie sie ab.</p></li>
                <li><p>Wählen Sie eine der verfügbaren Vorlagen aus.</p></li>
                <li><p>Wechseln Sie in den Simulationsmodus und passen Sie die Vorlage bei Bedarf an.</p></li>
            </ol>
        </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "CSV-Datei hochladen", label_visibility="collapsed"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.columnLabelMap = {norm(c): c for c in df.columns}
        st.session_state.data = df.to_dict(orient="records")

        st.session_state.uploaded_filename = uploaded_file.name

        if st.button("Senden", width="stretch"):
            st.session_state.data = df.to_dict(orient="records")
            st.switch_page("pages/template_selection.py")

    st.markdown(
        f"""
        <p class="explore-link">
            Sie haben noch keine Daten? 
            <a href="https://mobilithek.info/">Entdecken Sie Mobilithek</a>
        </p>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div class="right-container" style="background-image: url(data:image/svg+xml;base64,{b64})"></div>',
        unsafe_allow_html=True,
    )
