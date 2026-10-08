import streamlit as st
from ui import set_background
import sqlite3
import time

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide")

set_background()

st.markdown(
    """
    <style>
    .login-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        max-width: 500px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="login-box">
        <h2 style="margin-bottom: 0.3rem;">Login</h2>
        <p style="margin-top: 0;">Welcome back! Please sign in to continue.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")






email = st.text_input("Email")
password = st.text_input("Password", type="password")

col1, col2 = st.columns([1, 1])




with col1:
    
    if st.button("Login", use_container_width=True):
        if email and password:
                        
            conn = sqlite3.connect('database/database.db')
            
            c = conn.cursor()
            
            user = c.execute(""" 
                             SELECT id, name, age, address, email, phone, password, role, dob FROM users WHERE email = ? AND password = ?"""
                             , (email, password))
            
            user_data = user.fetchone()
            
            if user_data:
                
                st.session_state.user = user_data
                
                st.success("Login successful!")
                st.switch_page("pages/home.py")
                
            else:
                st.error("Invalid email or password.")
              
            conn.commit()
            conn.close()  
        else:
            st.error("Please fill in all the fields.")
            
            
with col2:
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("pages/home.py")
