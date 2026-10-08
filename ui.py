import streamlit as st


def set_background(image="marble.png"):
    # Image is served from static/ (server.enableStaticServing in .streamlit/config.toml).
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("app/static/""" + image + """");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
