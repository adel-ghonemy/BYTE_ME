import streamlit as st

# Forget who is logged in and empty the cart, then go back to Home.
st.session_state.clear()
st.rerun()
