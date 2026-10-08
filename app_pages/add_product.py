import sqlite3
import streamlit as st

st.markdown("<div class='banner'><h1>Add a product</h1></div>", unsafe_allow_html=True)

# The dropdowns show names, but the database needs ids.
# These dictionaries remember which id goes with which name.
conn = sqlite3.connect("database/database.db")
restaurant_ids = {}
for restaurant_id, restaurant_name in conn.execute("SELECT id, name FROM restaurant ORDER BY name").fetchall():
    restaurant_ids[restaurant_name] = restaurant_id
category_ids = {}
for category_id, category_name in conn.execute("SELECT id, name FROM categories ORDER BY name").fetchall():
    category_ids[category_name] = category_id
conn.close()

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name")
    restaurant_name = st.selectbox("Restaurant", list(restaurant_ids))
    category_name = st.selectbox("Category", list(category_ids))
    price = st.number_input("Price (EGP)", min_value=1)
    calories = st.number_input("Calories", min_value=0)
with col2:
    rating = st.number_input("Rating (1 to 5)", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
    stock = st.number_input("How many in stock", min_value=0)
    image_url = st.text_input("Image link (optional)")
    is_available = st.checkbox("Available to order", value=True)
description = st.text_area("Description")

if st.button("Add product", type="primary"):
    if name == "":
        st.error("Please type a name.")
    elif restaurant_name is None or category_name is None:
        st.error("Add a restaurant and a category first.")
    else:
        # The database keeps "available" as 1 for yes and 0 for no.
        if is_available:
            available_number = 1
        else:
            available_number = 0

        conn = sqlite3.connect("database/database.db")
        conn.execute(
            "INSERT INTO products (name, restaurant_id, category_id, calories, price, rating, description, image_url, stock, is_available) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, restaurant_ids[restaurant_name], category_ids[category_name], calories, price, rating,
             description, image_url, stock, available_number),
        )
        conn.commit()
        conn.close()
        st.success(name + " was added!")
