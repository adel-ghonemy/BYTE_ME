import sqlite3
import streamlit as st

st.markdown(
    "<div class='banner'><h1>Food Delivery</h1>"
    "<p>Find something delicious from a restaurant near you.</p></div>",
    unsafe_allow_html=True,
)

if st.session_state.user:
    st.write("Welcome, " + st.session_state.user["name"] + "!")
else:
    st.write("Welcome! Choose a restaurant.")

search = st.text_input("Search for a restaurant")

conn = sqlite3.connect("database/database.db")

# Build the list for the food type dropdown: "All" plus every type we have.
type_names = ["All"]
for row in conn.execute("SELECT DISTINCT type FROM restaurant ORDER BY type").fetchall():
    type_names.append(row[0])

chosen_type = st.selectbox("Choose food type", type_names)

# The % signs mean "anything before or after", so "piz" finds "Pizza King".
if chosen_type == "All":
    restaurants = conn.execute(
        "SELECT id, name, address, type FROM restaurant WHERE name LIKE ? ORDER BY name",
        ("%" + search + "%",),
    ).fetchall()
else:
    restaurants = conn.execute(
        "SELECT id, name, address, type FROM restaurant WHERE name LIKE ? AND type = ? ORDER BY name",
        ("%" + search + "%", chosen_type),
    ).fetchall()

conn.close()

st.write(str(len(restaurants)) + " restaurants found")

# Show the restaurants three in a row.
number = 0
for restaurant_id, name, address, food_type in restaurants:
    if number % 3 == 0:
        columns = st.columns(3)

    with columns[number % 3]:
        st.markdown(
            "<div class='card'><h3>" + name + "</h3><p>" + food_type + "</p><p>" + address + "</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("See menu", key="restaurant_" + str(restaurant_id)):
            st.session_state.restaurant_id = restaurant_id
            st.session_state.restaurant_name = name
            st.switch_page("app_pages/menu.py")

    number = number + 1
