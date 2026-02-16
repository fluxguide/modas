import streamlit as st
import pandas as pd
import base64
from components.vue_colour_picker import vue_color_picker

selected_color = vue_color_picker(label="Theme color", default="#010080")
if selected_color:
    st.write(f"You picked: {selected_color}")

# # MARK: Base Setup
# st.set_page_config(layout="wide")  # wide mode to use the whole screen

# with open("style.css") as f:
#     st.markdown(
#         f"<style>{f.read()}</style>", unsafe_allow_html=True
#     )

# with open("./assets/img/modas-side-img.svg", "r") as f:
#     svg_content = f.read()
# b64 = base64.b64encode(svg_content.encode()).decode()


# # MARK: Columns split
# col1, col2 = st.columns(2, gap="xxsmall")

# with col1:
#     st.markdown(
#         f"""
#         <div class="left-container">
#             <p>A brief Explanation here</p>
#             <p>Before you start please watch the video with instructions</p>
#             <h2>Upload File</h2>
#             <p>Select and upload the file of your choice</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#         text_alignment="center"
#     )

#     st.file_uploader("Upload CSV file", type="csv", label_visibility="collapsed")

#     st.markdown(
#         f"""
#         <p class="explore-link">
#             Do not have any data yet? 
#             <span style="color:{st.get_option("theme.primaryColor")}; font-weight:bold">Explore Mobilithek</span>
#         </p>
#         """,
#         unsafe_allow_html=True,
#         text_alignment="center"
#     )

# with col2:
#     st.markdown(
#         f'<div class="right-container" style="background-image: url(data:image/svg+xml;base64,{b64})"></div>',
#         unsafe_allow_html=True,
#     )


# # MARK: Future
# # Retrieving table data --> will need later
# # uploaded_files = st.file_uploader("Upload data", accept_multiple_files=True, type="csv")
# # for uploaded_file in uploaded_files:
# #     df = pd.read_csv(uploaded_file)
# #     edited_df = st.data_editor(df)