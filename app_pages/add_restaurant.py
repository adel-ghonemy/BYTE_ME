import sqlite3
import streamlit as st

st.markdown("<div class='banner'><h1>Add a restaurant</h1></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name")
    opendate = st.date_input("Opening date")
with col2:
    phone = st.text_input("Phone number")
    food_type = st.text_input("Food type (for example Pizza)")
address = st.text_input("Address")

if st.button("Add restaurant", type="primary"):
    conn = sqlite3.connect("database/database.db")
    name_taken = conn.execute("SELECT id FROM restaurant WHERE name = ?", (name,)).fetchone()
    phone_taken = conn.execute("SELECT id FROM restaurant WHERE phone = ?", (phone,)).fetchone()

    if name == "" or phone == "" or food_type == "" or address == "":
        st.error("Please fill in all the fields.")
    elif name_taken:
        st.error("A restaurant with this name already exists.")
    elif phone_taken:
        st.error("A restaurant with this phone number already exists.")
    else:
        conn.execute(
            "INSERT INTO restaurant (name, opendate, address, phone, type) VALUES (?, ?, ?, ?, ?)",
            (name, str(opendate), address, phone, food_type),
        )
        conn.commit()
        st.success(name + " was added!")

    conn.close()
