# Food Delivery

A small food delivery website, like Talabat. You pick a restaurant, put dishes in your cart, and place an order. Admins add restaurants and dishes and move orders along from "pending" to "completed".

## How it works

- The website is made with **Streamlit**, a Python library that turns a Python script into a web page.
- Everything is saved in one file, `database/database.db`, using **SQLite**, the small database that comes built into Python.
- `app.py` runs first every time. It sets the look of the app and builds the menu on the left. The menu only shows the pages you're allowed to open:
  - **Everyone:** Home, Menu, Log in, Register
  - **Logged in:** Cart, My orders, Log out
  - **Admins and restaurant owners:** Add restaurant, Add product, Add category, Manage orders
- Each screen is one Python file in `app_pages/`. Each one talks to the database on its own, with plain SQL.
- When you log in, the app remembers you in `st.session_state.user` (your id, name and role). Your cart is kept in `st.session_state.cart`.
- When you place an order, the app does five things:
  1. saves your address
  2. saves the order
  3. saves each dish in it
  4. saves the payment
  5. takes the dishes out of the stock

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501. Start it from this folder, because the app finds the database with the path `database/database.db`.

## Set up a new database

The app doesn't create the database by itself. To make a new one, run the SQL files in this order:

```bash
cd database
sqlite3 database.db < create_tables.sql
sqlite3 database.db < insert_user.SQL
sqlite3 database.db < insert_resturant.SQL
sqlite3 database.db < insert_categories.SQL
sqlite3 database.db < insert_products.SQL
sqlite3 database.db < insert_order.SQL
```

Each `insert_*.SQL` file **deletes** what is already in its table before adding the demo rows.

To make someone an admin:

```bash
sqlite3 database/database.db "UPDATE users SET role = 'admin' WHERE email = 'someone@example.com'"
```

## Deploy it

Put the folder on GitHub and deploy `app.py` on [Streamlit Community Cloud](https://streamlit.io/cloud). The database file goes along with the code. Any orders or sign-ups made on the website are lost whenever the app restarts or is deployed again.

## Limits

We kept the app simple on purpose. Here's what that means:

- **Passwords are saved as plain text.** Anyone who opens `database.db` can read every password.
- **Roles are set by hand.** Everyone who signs up is a customer. Admins and restaurant owners have to be set in the database (see above).
- **Restaurant owners can do everything admins can.** They can add dishes to any restaurant and change any order, not just their own.
- **There are no real payments.** Card and wallet orders are marked "paid" right away. Cash orders stay "pending", and nothing in the app ever changes that.
- **Reloading the page logs you out** and empties your cart, because both are only kept while the page is open.
- **One restaurant per order**, because one driver brings it.
- **Stock is checked when you order.** If two people buy the very last dish at the same moment, both orders can go through.
- **Each order saves its address as a new row**, so the same address can be saved many times.
- **Photos are web links.** If the link is broken, the picture is broken too.
- **The app only checks for problems that people often run into:** empty fields, an email or phone number that's already used, and not enough stock. Anything else shows Streamlit's red error box. If that happens in the middle of placing an order, the database can stay locked until the app is restarted.
