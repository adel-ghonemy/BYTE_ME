import sqlite3
import streamlit as st

st.markdown("<div class='banner'><h1>Add a category</h1></div>", unsafe_allow_html=True)

name = st.text_input("Name")

if st.button("Add category", type="primary"):
    conn = sqlite3.connect("database/database.db")
    name_taken = conn.execute("SELECT id FROM categories WHERE name = ?", (name,)).fetchone()

    if name == "":
        st.error("Please type a name.")
    elif name_taken:
        st.error("This category already exists.")
    else:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        st.success(name + " was added!")

    conn.close()
