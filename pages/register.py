import streamlit as st
from ui import set_background
import sqlite3
import time


st.set_page_config(page_title="Register", page_icon="📝", layout="wide")

set_background()

st.markdown(
    """
    <style>
    .register-box {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        max-width: 700px;
        margin: 0 auto 1rem auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="register-box">
        <h2 style="margin-bottom: 0.3rem;">Create an Account</h2>
        <p style="margin-top: 0;">Join us and enjoy a better experience.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


col1, col2 = st.columns(2)


with col1:
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=9, max_value=90)
    address = st.text_input("Address")
    email = st.text_input("Email")
with col2:
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    dob = st.date_input("Date of Birth")

col3, col4 = st.columns([1, 1])



with col3:


    if st.button("Register", use_container_width=True):
        
        if name and age and address and email and phone and password and dob:
            
            
            conn = sqlite3.connect('database/database.db')
            
            c = conn.cursor()
            
            try:
                c.execute("INSERT INTO users (name, age, address, email, phone, password, role, dob) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (name, age, address, email, phone, password, "customer", dob))
                conn.commit()
                st.success("Registration successful!")
                time.sleep(1)
                st.switch_page("pages/login.py")
            except sqlite3.IntegrityError:
                st.error("This email or phone number is already registered.")
            finally:
                conn.close()
            
        else:
            st.error("Please fill in all the fields.")



with col4:
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("pages/home.py")