import streamlit as st
from ui import set_background

st.set_page_config(page_title="Talabat Style Delivery", page_icon="🍽️", layout="wide")

set_background()

if "user" not in st.session_state:
	st.session_state.user = None

if "cart" not in st.session_state:
	st.session_state.cart = []

st.markdown("<div style='padding: 1rem 0;'>Loading your food experience...</div>", unsafe_allow_html=True)
# st.switch_page("/pages/home")
