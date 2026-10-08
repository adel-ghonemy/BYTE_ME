import sqlite3
import streamlit as st

st.markdown(
    "<div class='banner'><h1>Log in</h1><p>Welcome back! Please sign in to continue.</p></div>",
    unsafe_allow_html=True,
)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if email == "" or password == "":
        st.error("Please fill in all the fields.")
    else:
        conn = sqlite3.connect("database/database.db")
        row = conn.execute(
            "SELECT id, name, role FROM users WHERE email = ? AND password = ?",
            (email, password),
        ).fetchone()
        conn.close()

        if row is None:
            st.error("Wrong email or password.")
        else:
            st.session_state.user = {"id": row[0], "name": row[1], "role": row[2]}
            # Run the app again so the menu shows the pages this user can open.
            st.rerun()
