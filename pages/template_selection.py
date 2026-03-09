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
        {"label": "Vorlagen", "href": "/template_selection"},
        # {"label": "About MoDaS", "href": "/about_modas"},
    ],
    active_page="/template_selection",
    top_bar_right_button={"label": "Datei erneut hochladen", "href": "/"},
)

IMG_URL_BASE = "/app/static/img/Suite/Template_Previews"  # for clickable_images
IMG_FILE_BASE = "static/img/Suite/Template_Previews"  # for st.image local file read
GIF_FILE_BASE = "/app/static/gif"

templates_first_row = [
    {
        "key": "thuringia",
        "label": "ÖPNV-Erreichbarkeit von Points of Interest",
        "img_url": f"{IMG_URL_BASE}/Thuringia-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/Thuringia-Preview.png",
        "gif_file": f"{GIF_FILE_BASE}/Thuringia-Preview.gif",
        "description": "Diese Vorlage veranschaulicht die ÖPNV-Erreichbarkeit von Points of Interest, wie beispielsweise Rathäusern oder Schulen. Zur Visualisierung der Distanzen zwischen Points of Interest und Haltestellen werden 2D-Darstellungen sowie statische und interaktive Karten eingesetzt. Ziel ist es, Potenziale und Lücken in der Anbindung sichtbar zu machen.",
        "structure-interaction": " Zu Beginn führt ein Scrollytelling-Abschnitt mit klarer Nutzerführung durch die zentralen Erkenntnisse. Am Ende steht eine interaktive Karte zur freien Exploration. Eine erzählende Figur („Inge“) begleitet die Story und ordnet die Ergebnisse ein.",
        "data-requirements": "Name (optional), Stadt, Straße, Koordinaten (Lat/Long), Anzahl der Haltestellen in definierten Radien.",
        "suitable_for": "Diese Vorlage eignet sich zur Darstellung von Distanzen und zur Analyse der räumlichen Erreichbarkeit von Standorten, insbesondere im Kontext von Mobilität und Infrastruktur.",
    },
    {
        "key": "vrr",
        "label": "Veränderungen in Projekten",
        "img_url": f"{IMG_URL_BASE}/VRR-Preview.png",
        "gif_file": f"{GIF_FILE_BASE}/VRR-Preview.gif",
        "img_file": f"{IMG_FILE_BASE}/VRR-Preview.png",
        "description": "Diese Vorlage zeigt, wie sich z. B. Verkehrsunternehmen oder (Mobilitäts-) Projekte im Laufe der letzten Jahre verändert haben. Dies kann verschiedene Fachbereiche des Unternehmens betreffen, z. B. die Kundenkommunikation.",
        "structure-interaction": "Die Data Story folgt dem Scrollytelling-Prinzip (vertikales Scrollen), wobei verschiedene Visualisierungstypen wie Zeitstrahle und Kreisdiagramme eingesetzt werden.",
        "data-requirements": "Strukturierte Daten mit Jahresvergleichen, Daten und Fakten zum Projektablauf und Projektergebnissen",
        "suitable_for": "Diese Vorlage eignet sich besonders zur interaktiven Darstellung von Projektabläufen, z.B. der Veränderung der Kundenkommunikation in Verkehrsunternehmen in den letzten Jahren.",
    },
    {
        "key": "dresden",
        "label": "Städte in Bewegung",
        "img_url": f"{IMG_URL_BASE}/Dresden-Preview.png",
        "gif_file": f"{GIF_FILE_BASE}/Dresden-Preview.gif",
        "img_file": f"{IMG_FILE_BASE}/Dresden-Preview.png",
        "description": "Diese Vorlage basiert auf Umfragedaten in Städten und bereitet die meist komplexen Umfrageergebnisse verständlich und interaktiv auf. Ziel ist es, unterschiedliche Perspektiven und Nutzungsmuster sichtbar zu machen.",
        "structure-interaction": "Zu Beginn stehen den Rezipient*innen Auswahloptionen zur Verfügung, mit denen unterschiedliche Kategorien (z. B. Regionen, Merkmale oder Themenbereiche) ausgewählt werden können. Dabei kombiniert die Data Story vertikale und horizontale Scrollbewegungen im Stil einer interaktiven Scrollytelling-Erzählung. Außerdem fällt diese Vorlage durch ihren markanten Pixelstil auf.",
        "data-requirements": "Strukturierte Umfragedaten mit Kategorien (z. B. Altersgruppen, Stadtteile, Verkehrsmittel), Kennzahlen (z. B. Anteile, Häufigkeiten), Bewertungsdimensionen (z. B. Zufriedenheit, Sicherheit).",
        "suitable_for": "Diese Vorlage eignet sich besonders zur interaktiven Darstellung und Differenzierung von Umfrageergebnissen. Sie ist ideal, wenn verschiedene Gruppen (z. B. Altersgruppen, Regionen oder Nutzungstypen) vergleichend betrachtet und durch Nutzerauswahl explorierbar gemacht werden sollen.",
    },
]

templates_second_row = [
    {
        "key": "story4",
        "label": "Story 4",
        "img_url": f"{IMG_URL_BASE}/Dortmund-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/Dortmund-Preview.png",
        "gif_file": f"{GIF_FILE_BASE}/Thuringia-Preview.gif",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "structure-interaction": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "data-requirements": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "suitable_for": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
    },
    {
        "key": "story5",
        "label": "Story 5",
        "img_url": f"{IMG_URL_BASE}/Ilmenau-Preview.png",
        "img_file": f"{IMG_FILE_BASE}/Ilmenau-Preview.png",
        "gif_file": f"{GIF_FILE_BASE}/Thuringia-Preview.gif",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "structure-interaction": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "data-requirements": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
        "suitable_for": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut placerat tortor. Proin lorem mauris, pulvinar eget elementum eget, efficitur a ante. Donec luctus, metus ut fermentum gravida, tellus neque rutrum leo, aliquam fermentum velit nisl non lacus. ",
    },
]

uploaded_filename = html.escape(st.session_state.get("uploaded_filename", ""))

st.markdown(
    f"""
    <div class="template-page-instructions">
        <p>
            <span>{uploaded_filename}</span> wurde erfolgreich hochgeladen.
        </p>
        <h4>
            Klicken Sie auf eine Vorlage, um Details anzuzeigen und das Layout für Ihre Story-Simulation auszuwählen.
        </h4>
    </div>
    """,
    unsafe_allow_html=True,
)

if "last_clicked_row_1" not in st.session_state:
    st.session_state.last_clicked_row_1 = -1
if "last_clicked_row_2" not in st.session_state:
    st.session_state.last_clicked_row_2 = -1

clicked1 = clickable_images(
    [t["img_url"] for t in templates_first_row],
    titles=[t["label"] for t in templates_first_row],
    div_style={
        "display": "grid",
        "gridTemplateColumns": "repeat(3, 1fr)",
        "gap": "50px",
        "margin": "0 5vw",
        "padding-top": "40px",
        "padding-bottom": "10px",
    },
    img_style={
        "width": "90%",
        "height": "fit-content",
        "objectFit": "cover",
        "borderRadius": "12px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.14)",
        "cursor": "pointer",
    },
    key="templates_row_1",
)

if clicked1 > -1 and clicked1 != st.session_state.last_clicked_row_1:
    st.session_state.last_clicked_row_1 = clicked1
    st.session_state.preview_template = templates_first_row[clicked1]["key"]

st.markdown(
    """
    <div class="template-caption-grid">
    """
    + "".join(
        f'<div class="template-caption">{t["label"]}</div>' for t in templates_first_row
    )
    + """
    </div>
    """,
    unsafe_allow_html=True,
)

# clicked2 = clickable_images(
#     [t["img_url"] for t in templates_second_row],
#     titles=[t["label"] for t in templates_second_row],
#     div_style={
#         "display": "grid",
#         "gridTemplateColumns": "repeat(3, 1fr)",
#         "gap": "50px",
#         "margin": "0 5vw",
#         "padding-bottom": "10px",
#     },
#     img_style={
#         "width": "90%",
#         "height": "fit-content",
#         "objectFit": "cover",
#         "borderRadius": "12px",
#         "boxShadow": "0 2px 6px rgba(0,0,0,0.14)",
#         "cursor": "pointer",
#     },
#     key="templates_row_2",
# )

# if clicked2 > -1 and clicked2 != st.session_state.last_clicked_row_2:
#     st.session_state.last_clicked_row_2 = clicked2
#     st.session_state.preview_template = templates_second_row[clicked2]["key"]

# st.markdown(
#     """
#     <div class="template-caption-grid">
#     """
#     + "".join(
#         f'<div class="template-caption">{t["label"]}</div>'
#         for t in templates_second_row
#     )
#     + """
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


template_by_key_all = {
    t["key"]: t for t in (templates_first_row + templates_second_row)
}
preview_key = st.session_state.get("preview_template")

if preview_key and preview_key in template_by_key_all:
    tpl = template_by_key_all[preview_key]

    @st.dialog(f"Data Story: {tpl['label']}")
    def template_dialog():
        left, right = st.columns([1.15, 1], gap="large")

        with left:
            st.markdown(
                f"""
                <div class="gif-top-align">
                    <img src="{tpl["gif_file"]}" alt="Preview GIF">
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            st.markdown(
                f"""
                <div class="template-dialog-text">
                    <h3>Über die Vorlage</h3>
                    <p>{tpl["description"]}</p>
                    <h3>Aufbau und Interaktion</h3>
                    <p>{tpl["structure-interaction"]}</p>
                    <h3>Benötigte Daten</h3>
                    <p>{tpl["data-requirements"]}</p>
                    <h3>Passend für</h3>
                    <p>{tpl["suitable_for"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Wählen Sie diese Vorlage aus",
                width="stretch",
                key=f"tpl_select_{tpl['key']}",
            ):
                st.session_state.selected_template = tpl["key"]
                st.session_state.selected_template_label = tpl["label"]
                st.session_state.preview_template = None
                st.switch_page("pages/simulation_mode.py")

    template_dialog()

st.markdown("</div>", unsafe_allow_html=True)
