import sqlite3
import time
import streamlit as st

# The three ways to pay that the database allows.
PAYMENT_METHODS = ["cash", "card", "wallet"]

st.markdown(
    "<div class='banner'><h1>Your cart</h1><p>Review your order before checkout.</p></div>",
    unsafe_allow_html=True,
)

if len(st.session_state.cart) == 0:
    st.info("Your cart is empty. Pick some food from a menu.")
    st.stop()

total = 0
for item in st.session_state.cart:
    line_price = item["price"] * item["quantity"]
    total = total + line_price

    left, right = st.columns([5, 1])
    with left:
        st.markdown(
            "<div class='card'><strong>" + item["name"] + "</strong><br>"
            + "Quantity: " + str(item["quantity"]) + "<br>"
            + "<strong>" + str(line_price) + " EGP</strong></div>",
            unsafe_allow_html=True,
        )
    with right:
        if st.button("Remove", key="remove_" + str(item["id"])):
            st.session_state.cart.remove(item)
            st.rerun()

st.subheader("Total: " + str(total) + " EGP")

address = st.text_input("Delivery address")
notes = st.text_area("Notes for the restaurant (optional)")
payment_method = st.radio("How will you pay?", PAYMENT_METHODS, horizontal=True)

if st.button("Place order", type="primary"):
    conn = sqlite3.connect("database/database.db")

    # Check the stock again, in case someone else bought the food in the meantime.
    problem = ""
    for item in st.session_state.cart:
        stock = conn.execute("SELECT stock FROM products WHERE id = ?", (item["id"],)).fetchone()[0]
        if item["quantity"] > stock:
            problem = "Sorry, only " + str(stock) + " " + item["name"] + " left."

    if address == "":
        st.error("Please type your delivery address.")
    elif problem != "":
        st.error(problem)
    else:
        user_id = st.session_state.user["id"]

        # Cash is paid at the door, so it stays "pending". Card and wallet count as paid now.
        if payment_method == "cash":
            payment_status = "pending"
        else:
            payment_status = "paid"

        # Save the address, so the order can point to it.
        cursor = conn.execute(
            "INSERT INTO user_addresses (user_id, address) VALUES (?, ?)",
            (user_id, address),
        )
        address_id = cursor.lastrowid

        # The time in milliseconds makes every order number different,
        # even when two people press the button in the same second.
        order_number = "ORDER" + str(int(time.time() * 1000))
        cursor = conn.execute(
            "INSERT INTO orders (user_id, restaurant_id, user_address_id, order_number, notes, total_price, payment_status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, st.session_state.cart[0]["restaurant_id"], address_id, order_number, notes, total, payment_status),
        )
        order_id = cursor.lastrowid

        for item in st.session_state.cart:
            conn.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, item["id"], item["quantity"], item["price"]),
            )
            # Take the food we just sold out of the stock.
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (item["quantity"], item["id"]),
            )

        conn.execute(
            "INSERT INTO payments (order_id, amount, payment_method, status) VALUES (?, ?, ?, ?)",
            (order_id, total, payment_method, payment_status),
        )

        conn.commit()
        st.session_state.cart = []
        st.success("Order " + order_number + " placed! You can follow it in My orders.")

    conn.close()
