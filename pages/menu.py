import sqlite3
import streamlit as st
from ui import set_background

st.set_page_config(page_title="Menu", page_icon="🍔", layout="wide")

set_background()

st.markdown(
    """
    <style>
    h1, h2, h3 {
        color: #2f241d;
    }
    .menu-header {
        background: linear-gradient(120deg, #e85d04, #f48c06);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 18px;
        margin: 0.5rem 0 1.25rem 0;
    }
    .menu-header h1, .menu-header p {
        color: white;
        margin: 0;
    }
    .product-card {
        background: white;
        border: 1px solid #f0dfcc;
        border-radius: 14px;
        padding: 1rem;
        min-height: 205px;
        box-shadow: 0 5px 16px rgba(80, 45, 20, 0.06);
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

if "restaurant_id" not in st.session_state:
    st.error("Please choose a restaurant first.")
    st.stop()

restaurant_id = st.session_state.restaurant_id
restaurant_name = st.session_state.restaurant_name

st.markdown(
    "<div class='menu-header'><h1>" + restaurant_name
    + " menu</h1><p>Choose your food. Items in cart: "
    + str(len(st.session_state.cart)) + "</p></div>",
    unsafe_allow_html=True,
)

search = st.text_input("Search for food")

conn = sqlite3.connect("database/database.db")
products = conn.execute(
    "SELECT id, name, price, description FROM products "
    "WHERE restaurant_id = ? AND name LIKE ? "
    "AND is_available = 1 AND stock > 0",
    (restaurant_id, "%" + search + "%")
).fetchall()
conn.close()

for number, product in enumerate(products):
    if number % 3 == 0:
        columns = st.columns(3)

    with columns[number % 3]:
        st.markdown(
            "<div class='product-card'><h3>" + product[1]
            + "</h3><p>" + product[3] + "</p><strong>"
            + str(product[2]) + " EGP</strong></div>",
            unsafe_allow_html=True,
        )
        st.write("")
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=10,
            value=1,
            key="quantity_" + str(product[0])
        )

        if st.button("Add to cart", key="add_" + str(product[0])):
            can_add = True

            if len(st.session_state.cart) > 0:
                old_restaurant = st.session_state.cart[0]["restaurant_id"]
                if old_restaurant != restaurant_id:
                    can_add = False
                    st.error("You can only order from one restaurant.")

            if can_add:
                found = False

                for item in st.session_state.cart:
                    if item["id"] == product[0]:
                        item["quantity"] = item["quantity"] + quantity
                        found = True

                if found == False:
                    st.session_state.cart.append({
                        "id": product[0],
                        "name": product[1],
                        "price": product[2],
                        "quantity": quantity,
                        "restaurant_id": restaurant_id,
                    })

                st.success("Added to cart")

if st.button("Open cart"):
    st.switch_page("pages/cart.py")