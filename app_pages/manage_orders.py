import sqlite3
import streamlit as st

# The order steps the database allows, in the order they happen.
STATUSES = ["pending", "preparing", "completed", "canceled"]

st.markdown(
    "<div class='banner'><h1>Manage orders</h1><p>Move each order along as it gets cooked and delivered.</p></div>",
    unsafe_allow_html=True,
)

# Join the tables so each order shows who ordered, from where, and to which address.
conn = sqlite3.connect("database/database.db")
orders = conn.execute(
    "SELECT orders.id, orders.order_number, orders.status, orders.total_price, orders.payment_status, "
    "orders.notes, users.name, restaurant.name, user_addresses.address "
    "FROM orders "
    "JOIN users ON users.id = orders.user_id "
    "JOIN restaurant ON restaurant.id = orders.restaurant_id "
    "LEFT JOIN user_addresses ON user_addresses.id = orders.user_address_id "
    "ORDER BY orders.id DESC"
).fetchall()
conn.close()

if len(orders) == 0:
    st.info("There are no orders yet.")

for order_id, order_number, status, total_price, payment_status, notes, customer, restaurant, address in orders:
    text = "<div class='card'><h3>" + order_number + "</h3><p>"
    text = text + customer + " ordered from " + restaurant + "<br>"
    text = text + "Total: " + str(total_price) + " EGP · Payment: " + payment_status + "<br>"
    if address:
        text = text + "Deliver to: " + address + "<br>"
    if notes:
        text = text + "Notes: " + notes
    text = text + "</p></div>"
    st.markdown(text, unsafe_allow_html=True)

    left, right = st.columns([3, 1])
    with left:
        new_status = st.selectbox(
            "Status", STATUSES, index=STATUSES.index(status), key="status_" + str(order_id)
        )
    with right:
        if st.button("Save", key="save_" + str(order_id)):
            conn = sqlite3.connect("database/database.db")
            conn.execute(
                "UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_status, order_id),
            )
            conn.commit()
            conn.close()
            st.success("Saved")
