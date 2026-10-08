import sqlite3
import streamlit as st
from ui import set_background

st.set_page_config(page_title="Food Delivery", page_icon="🍽️", layout="wide")

set_background()

st.markdown(
    """
    <style>
    h1, h2, h3 {
        color: #2f241d;
    }
    .hero {
        background: linear-gradient(120deg, #e85d04, #f48c06);
        color: white;
        padding: 2.2rem;
        border-radius: 18px;
        margin: 0.5rem 0 1.5rem 0;
        box-shadow: 0 12px 30px rgba(232, 93, 4, 0.2);
    }
    .hero h1, .hero p {
        color: white;
        margin: 0;
    }
    .restaurant-card {
        background: white;
        border: 1px solid #f0dfcc;
        border-radius: 14px;
        padding: 1rem;
        min-height: 150px;
        box-shadow: 0 5px 16px rgba(80, 45, 20, 0.06);
    }
    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #e85d04;
        color: #c2410c;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background: #fff0df;
        border-color: #c2410c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "user" not in st.session_state:
    st.session_state.user = None

if "cart" not in st.session_state:
    st.session_state.cart = []


st.markdown(
    """
    <div class="hero">
        <h1>Food Delivery</h1>
        <p>Find something delicious from a restaurant near you.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.user:
    st.write("Welcome, " + st.session_state.user[1])
else:
    st.write("Welcome! Choose a restaurant.")

col1, col2 = st.columns(2)

with col1:
    if st.button("My orders", use_container_width=True):
        st.switch_page("pages/orders.py")

with col2:
    if st.button("Cart", use_container_width=True):
        st.switch_page("pages/cart.py")

search = st.text_input("Search for a restaurant")

conn = sqlite3.connect("database/database.db")
types = conn.execute("SELECT DISTINCT type FROM restaurant ORDER BY type").fetchall()
type_names = ["All"]

for restaurant_type in types:
    type_names.append(restaurant_type[0])

chosen_type = st.selectbox("Choose food type", type_names)

if chosen_type == "All":
    restaurants = conn.execute(
        "SELECT id, name, address, type FROM restaurant "
        "WHERE name LIKE ? ORDER BY name",
        ("%" + search + "%",)
    ).fetchall()
else:
    restaurants = conn.execute(
        "SELECT id, name, address, type FROM restaurant "
        "WHERE name LIKE ? AND type = ? ORDER BY name",
        ("%" + search + "%", chosen_type)
    ).fetchall()

conn.close()


st.write(str(len(restaurants)) + " restaurants found")

for number, restaurant in enumerate(restaurants):
    if number % 3 == 0:
        columns = st.columns(3)

    with columns[number % 3]:
        st.markdown(
            "<div class='restaurant-card'><h3>" + restaurant[1]
            + "</h3><p>" + restaurant[3] + "</p><p>"
            + restaurant[2] + "</p></div>",
            unsafe_allow_html=True,
        )
        st.write("")

        if st.button("See menu", key="restaurant_" + str(restaurant[0])):
            st.session_state.restaurant_id = restaurant[0]
            st.session_state.restaurant_name = restaurant[1]
            st.switch_page("pages/menu.py")
