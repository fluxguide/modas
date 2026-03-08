import streamlit as st
import pandas as pd
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

col1, col2 = st.columns(2, gap="small")

with col1:
    primary = st.get_option("theme.primaryColor")

    st.markdown(
        """
        <div class="left-container">
            <h1>Mobilitätsdaten-Story-Suite (MoDaS)</h1>
            <p>Wie lassen sich Mobilitätsdaten verständlich und effektiv vermitteln? Als Technologiepartner für das mfund-Projekt MoDaS haben wir eine Plattform entwickelt, die abstrakte Mobilitätsdaten in verständliche Storytelling-Formate übersetzt.</p>
            <p>Gemeinsam mit unserem Forschungspartner TU Ilmenau haben wir eine „Mobility Data Story Suite“ entwickelt, die Verkehrsdaten durch digitales Storytelling visualisiert. Die Zielgruppe sind Mobilitätsplaner, politische Entscheidungsträger und Bürger. Die Mobility Data Story Suite macht komplexe Daten mithilfe innovativer Storytelling-Methoden interaktiv zugänglich und verbessert so die Effizienz von Mobilitätsplanungsprozessen. Übersetzt mit DeepL.com (kostenlose Version)</p>
            <h3>Sind Sie bereit, Ihre eigene Geschichte zu schreiben?</h3>
            <ol>
                <li><p>Laden Sie Ihre Datendatei hoch und senden Sie sie ab.</p></li>
                <li><p>Wählen Sie eine der verfügbaren Vorlagen aus.</p></li>
                <li><p>Wechseln Sie in den Simulationsmodus und nehmen Sie bei Bedarf einige Änderungen an der Vorlage vor.</p></li>
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
