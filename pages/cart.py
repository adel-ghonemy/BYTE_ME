import sqlite3
import time
import streamlit as st
from ui import set_background

st.set_page_config(page_title="Cart", page_icon="🛒", layout="wide")

set_background()

st.markdown(
    """
    <style>
    h1, h2, h3 { color: #2f241d; }
    .cart-header {
        background: linear-gradient(120deg, #e85d04, #f48c06);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 18px;
        margin: 0.5rem 0 1.5rem 0;
    }
    .cart-header h1, .cart-header p { color: white; margin: 0; }
    .cart-item {
        background: white;
        border: 1px solid #f0dfcc;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.7rem;
    }
    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #e85d04;
        color: #c2410c;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "cart" not in st.session_state:
    st.session_state.cart = []

st.markdown(
    "<div class='cart-header'><h1>Your cart</h1>"
    "<p>Review your order before checkout.</p></div>",
    unsafe_allow_html=True,
)

if len(st.session_state.cart) == 0:
    st.info("Your cart is empty.")
    st.stop()

total = 0

for item in st.session_state.cart:
    st.markdown(
        "<div class='cart-item'><strong>" + item["name"]
        + "</strong><br>Quantity: " + str(item["quantity"])
        + "<br><strong>" + str(item["price"] * item["quantity"])
        + " EGP</strong></div>",
        unsafe_allow_html=True,
    )
    total = total + item["price"] * item["quantity"]

st.subheader("Total: " + str(total) + " EGP")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in before checkout.")
    st.stop()

if st.button("Checkout"):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    order_number = "ORDER" + str(int(time.time()))
    restaurant_id = st.session_state.cart[0]["restaurant_id"]

    cursor.execute(
        "INSERT INTO orders (user_id, restaurant_id, order_number, total_price) VALUES (?, ?, ?, ?)",
        (st.session_state.user[0], restaurant_id, order_number, total),
    )
    order_id = cursor.lastrowid

    for item in st.session_state.cart:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            (order_id, item["id"], item["quantity"], item["price"]),
        )

    conn.commit()
    conn.close()
    st.session_state.cart = []
    st.success("Order created")