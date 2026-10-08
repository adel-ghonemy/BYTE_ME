import sqlite3
import streamlit as st
from ui import set_background

st.set_page_config(page_title="Orders", page_icon="📦", layout="wide")

set_background()

st.markdown(
    """
    <style>
    h1, h2, h3 { color: #2f241d; }
    .orders-header {
        background: linear-gradient(120deg, #e85d04, #f48c06);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 18px;
        margin: 0.5rem 0 1.5rem 0;
    }
    .orders-header h1, .orders-header p { color: white; margin: 0; }
    .order-card {
        background: white;
        border: 1px solid #f0dfcc;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 5px 16px rgba(80, 45, 20, 0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in first.")
    st.stop()

st.markdown(
    "<div class='orders-header'><h1>Your orders</h1>"
    "<p>See your recent deliveries and order status.</p></div>",
    unsafe_allow_html=True,
)

conn = sqlite3.connect("database/database.db")
orders = conn.execute(
    "SELECT order_number, status, total_price, created_at "
    "FROM orders WHERE user_id = ? ORDER BY id DESC",
    (st.session_state.user[0],)
).fetchall()
conn.close()

if len(orders) == 0:
    st.info("You have no orders yet.")

for order in orders:
    st.markdown(
        "<div class='order-card'><h3>" + order[0]
        + "</h3><p>Status: " + order[1]
        + "<br>Total: " + str(order[2]) + " EGP"
        + "<br>Date: " + str(order[3]) + "</p></div>",
        unsafe_allow_html=True,
    )
