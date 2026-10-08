import sqlite3
import streamlit as st

st.markdown(
    "<div class='banner'><h1>Your orders</h1><p>See your recent deliveries and order status.</p></div>",
    unsafe_allow_html=True,
)

# Newest orders first.
conn = sqlite3.connect("database/database.db")
orders = conn.execute(
    "SELECT order_number, status, total_price, payment_status, notes, created_at "
    "FROM orders WHERE user_id = ? ORDER BY id DESC",
    (st.session_state.user["id"],),
).fetchall()
conn.close()

if len(orders) == 0:
    st.info("You have no orders yet.")

for order_number, status, total_price, payment_status, notes, created_at in orders:
    text = "<div class='card'><h3>" + order_number + "</h3><p>"
    text = text + "Status: " + status + "<br>"
    text = text + "Total: " + str(total_price) + " EGP<br>"
    text = text + "Payment: " + payment_status + "<br>"
    if notes:
        text = text + "Notes: " + notes + "<br>"
    text = text + "Date: " + str(created_at) + "</p></div>"
    st.markdown(text, unsafe_allow_html=True)
