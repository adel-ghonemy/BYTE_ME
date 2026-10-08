import sqlite3
import time
import streamlit as st

st.markdown(
    "<div class='banner'><h1>Create an account</h1><p>Join us and enjoy a better experience.</p></div>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=9, max_value=90)
    address = st.text_input("Address")
    email = st.text_input("Email")
with col2:
    phone = st.text_input("Phone number")
    password = st.text_input("Password", type="password")
    dob = st.date_input("Date of birth")

if st.button("Register", type="primary"):
    conn = sqlite3.connect("database/database.db")
    email_taken = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    phone_taken = conn.execute("SELECT id FROM users WHERE phone = ?", (phone,)).fetchone()
    conn.close()

    if name == "" or address == "" or email == "" or phone == "" or password == "":
        st.error("Please fill in all the fields.")
    elif email_taken:
        st.error("This email is already registered.")
    elif phone_taken:
        st.error("This phone number is already registered.")
    else:
        # Everyone starts as a customer. Admins are set by hand in the database.
        conn = sqlite3.connect("database/database.db")
        conn.execute(
            "INSERT INTO users (name, age, address, email, phone, password, role, dob) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, age, address, email, phone, password, "customer", str(dob)),
        )
        conn.commit()
        conn.close()
        st.success("Registration successful! Taking you to log in...")
        # Wait a moment so the message can be read.
        time.sleep(1)
        st.switch_page("app_pages/login.py")
