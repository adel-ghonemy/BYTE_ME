import sqlite3
import time
import streamlit as st

# The words people see on the payment pills, and the word the database keeps for each.
PAYMENT_METHODS = {
    "💵 Cash on delivery": "cash",
    "💳 Card": "card",
    "📱 Mobile wallet": "wallet",
}

# Egyptian phone numbers have 11 digits, like 01012345678.
PHONE_LENGTH = 11

st.markdown(
    "<div class='banner'><h1>Your order</h1><p>Check your food, tell us where to bring it, and pay.</p></div>",
    unsafe_allow_html=True,
)

if len(st.session_state.cart) == 0:
    st.info("Your cart is empty. Pick some food from a menu.")
    st.stop()

# Look up the restaurant's name and the user's saved phone and address, to fill in the form.
conn = sqlite3.connect("database/database.db")
restaurant_name = conn.execute(
    "SELECT name FROM restaurant WHERE id = ?", (st.session_state.cart[0]["restaurant_id"],)
).fetchone()[0]
saved_phone, saved_address = conn.execute(
    "SELECT phone, address FROM users WHERE id = ?", (st.session_state.user["id"],)
).fetchone()
conn.close()

# Some older accounts have no address saved, so we start with an empty box for them.
if saved_address is None:
    saved_address = ""

left, right = st.columns([3, 2], gap="large")

with left:
    # ---------- The food ----------
    st.subheader("🛒 Your food from " + restaurant_name)

    for item in st.session_state.cart:
        name_col, minus_col, count_col, plus_col, bin_col = st.columns([5, 1, 1, 1, 1], vertical_alignment="center")
        with name_col:
            st.markdown("**" + item["name"] + "**  \n" + str(item["price"]) + " EGP each")
        with minus_col:
            if st.button("➖", key="minus_" + str(item["id"])):
                # Taking away the last one takes the dish out of the cart.
                if item["quantity"] == 1:
                    st.session_state.cart.remove(item)
                else:
                    item["quantity"] = item["quantity"] - 1
                st.rerun()
        with count_col:
            st.markdown("### " + str(item["quantity"]))
        with plus_col:
            if st.button("➕", key="plus_" + str(item["id"])):
                # We can't sell more than the restaurant has.
                if item["quantity"] < item["stock"]:
                    item["quantity"] = item["quantity"] + 1
                    st.rerun()
                else:
                    st.toast("Sorry, only " + str(item["stock"]) + " left.")
        with bin_col:
            if st.button("🗑️", key="remove_" + str(item["id"])):
                st.session_state.cart.remove(item)
                st.rerun()

    st.divider()

    # ---------- Where to bring it ----------
    st.subheader("🚚 Delivery details")
    city_col, phone_col = st.columns(2)
    with city_col:
        city = st.text_input("City")
    with phone_col:
        phone = st.text_input("Phone", value=saved_phone)
    address = st.text_area("Full address (street, building, floor, flat)", value=saved_address)
    notes = st.text_area("Delivery notes (optional)", placeholder="For example: ring the bell twice")

    st.divider()

    # ---------- How to pay ----------
    st.subheader("💰 Payment method")
    payment_label = st.pills(
        "Choose how to pay", list(PAYMENT_METHODS), default="💵 Cash on delivery", required=True
    )
    payment_method = PAYMENT_METHODS[payment_label]

    # Card and wallet need a few more details. We only check them; we never save them.
    if payment_method == "card":
        card_name = st.text_input("Name on card")
        card_number = st.text_input("Card number", placeholder="1234 5678 9012 3456")
        expiry_col, cvv_col = st.columns(2)
        with expiry_col:
            card_expiry = st.text_input("Expiry date", placeholder="MM/YY")
        with cvv_col:
            card_cvv = st.text_input("CVV", type="password", placeholder="123")
    if payment_method == "wallet":
        wallet_phone = st.text_input("Wallet phone number", value=phone)

with right:
    # ---------- Order summary ----------
    total = 0
    summary = "<div class='card'><h3>🧾 Order summary</h3><p>From <strong>" + restaurant_name + "</strong></p>"
    for item in st.session_state.cart:
        line_price = item["price"] * item["quantity"]
        total = total + line_price
        summary = summary + "<p>" + str(item["quantity"]) + " × " + item["name"] + " — " + str(line_price) + " EGP</p>"
    summary = summary + "<hr>"
    if city != "" or address != "":
        summary = summary + "<p>📍 " + address + ", " + city + "</p>"
    summary = summary + "<p>📞 " + phone + "</p>"
    summary = summary + "<p>Paying with " + payment_label + "</p>"
    summary = summary + "<h3>Total: " + str(total) + " EGP</h3></div>"
    st.markdown(summary, unsafe_allow_html=True)

    place_order = st.button("Place order", type="primary", width="stretch")

if place_order:
    # Check everything the user typed. The first problem we find is the one we show.
    problem = ""
    if city == "" or address == "" or phone == "":
        problem = "Please fill in the city, full address and phone."
    elif not phone.isdigit() or len(phone) != PHONE_LENGTH:
        problem = "The phone number should be " + str(PHONE_LENGTH) + " digits, like 01012345678."
    elif payment_method == "card":
        # People often type spaces between the groups of numbers, so we take them out first.
        digits = card_number.replace(" ", "")
        if card_name == "" or not digits.isdigit() or len(digits) != 16:
            problem = "Please type the name on the card and its 16-digit number."
        elif len(card_expiry) != 5 or card_expiry[2] != "/":
            problem = "Please type the expiry date like 08/27."
        elif not card_cvv.isdigit() or len(card_cvv) != 3:
            problem = "The CVV is the 3 digits on the back of the card."
    elif payment_method == "wallet":
        if not wallet_phone.isdigit() or len(wallet_phone) != PHONE_LENGTH:
            problem = "The wallet phone number should be " + str(PHONE_LENGTH) + " digits."

    conn = sqlite3.connect("database/database.db")

    # Check the stock again, in case someone else bought the food in the meantime.
    if problem == "":
        for item in st.session_state.cart:
            stock = conn.execute("SELECT stock FROM products WHERE id = ?", (item["id"],)).fetchone()[0]
            if item["quantity"] > stock:
                problem = "Sorry, only " + str(stock) + " " + item["name"] + " left."

    if problem != "":
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
            "INSERT INTO user_addresses (user_id, address, city, phone) VALUES (?, ?, ?, ?)",
            (user_id, address, city, phone),
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
        st.balloons()

    conn.close()
