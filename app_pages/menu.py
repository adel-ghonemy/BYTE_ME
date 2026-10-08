import sqlite3
import streamlit as st

if "restaurant_id" not in st.session_state:
    st.info("Choose a restaurant on the Home page first.")
    st.stop()

restaurant_id = st.session_state.restaurant_id
restaurant_name = st.session_state.restaurant_name

st.markdown(
    "<div class='banner'><h1>" + restaurant_name + " menu</h1>"
    "<p>Items in your cart: " + str(len(st.session_state.cart)) + "</p></div>",
    unsafe_allow_html=True,
)

search = st.text_input("Search for food")

# Only show dishes that are switched on and still in stock.
conn = sqlite3.connect("database/database.db")
products = conn.execute(
    "SELECT id, name, price, description, calories, rating, image_url, stock FROM products "
    "WHERE restaurant_id = ? AND name LIKE ? AND is_available = 1 AND stock > 0",
    (restaurant_id, "%" + search + "%"),
).fetchall()
conn.close()

if len(products) == 0:
    st.info("No dishes found.")

if st.session_state.user is None:
    st.info("Log in to order.")

# Show the dishes three in a row.
number = 0
for product_id, name, price, description, calories, rating, image_url, stock in products:
    if number % 3 == 0:
        columns = st.columns(3)

    with columns[number % 3]:
        # Every photo gets the same size box, so the cards line up.
        if image_url:
            photo = "<div class='dish-photo' style=\"background-image: url('" + image_url + "')\"></div>"
        else:
            photo = "<div class='dish-photo no-photo'>🍽️</div>"

        # One star for each rating point, so 4.6 shows as ★★★★★ 4.6.
        stars = "★" * round(rating)
        st.markdown(
            "<div class='card'>" + photo + "<h3>" + name + "</h3>"
            + "<p>" + (description or "") + "</p>"
            + "<p>" + stars + " " + str(rating) + " · " + str(calories) + " kcal</p>"
            + "<strong>" + str(price) + " EGP</strong></div>",
            unsafe_allow_html=True,
        )

        # Guests can look, but only logged-in people can order.
        if st.session_state.user:
            quantity = st.number_input(
                "Quantity", min_value=1, max_value=stock, value=1, key="quantity_" + str(product_id)
            )

            if st.button("Add to cart", key="add_" + str(product_id), type="primary"):
                # How many of this dish are already in the cart?
                already_in_cart = 0
                for item in st.session_state.cart:
                    if item["id"] == product_id:
                        already_in_cart = item["quantity"]

                # A cart can only hold food from one restaurant, because one driver brings it.
                if len(st.session_state.cart) > 0 and st.session_state.cart[0]["restaurant_id"] != restaurant_id:
                    st.error("You can only order from one restaurant at a time.")
                elif already_in_cart + quantity > stock:
                    st.error("Sorry, only " + str(stock) + " left.")
                elif already_in_cart > 0:
                    for item in st.session_state.cart:
                        if item["id"] == product_id:
                            item["quantity"] = item["quantity"] + quantity
                    st.success("Added to cart")
                else:
                    st.session_state.cart.append({
                        "id": product_id,
                        "name": name,
                        "price": price,
                        "quantity": quantity,
                        "stock": stock,
                        "restaurant_id": restaurant_id,
                    })
                    st.success("Added to cart")

    number = number + 1
