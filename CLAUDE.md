# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Talabat-style food delivery app built with Streamlit (1.64) and a local SQLite database. There is no build step, no dependency manifest, no test suite, no linter config, and the directory is not a git repository.

## Running

```bash
streamlit run app.py        # serves on http://localhost:8501
```

Run from the repo root: every page opens the DB with the relative path `database/database.db` and navigates with `st.switch_page("pages/<name>.py")`, so both break if the working directory is different.

## Architecture

- **Multipage via the `pages/` directory**, not `st.navigation`. `app.py` is the entry point: it sets up session state and renders the background. Each file in `pages/` is a standalone script that re-runs top to bottom on every interaction and calls its own `st.set_page_config`.
- **Almost no shared code.** The only shared module is `ui.py`, whose `set_background()` every page calls just after `st.set_page_config`. Each page still opens its own `sqlite3` connection, writes raw SQL, and adds its own `<style>` block through `st.markdown(..., unsafe_allow_html=True)`. Page CSS such as `.hero-box` and the orange gradient header is copy-pasted between pages, so changing that look means editing every page.
- **Background image:** `set_background()` points `.stApp` at `app/static/marble.png`. This works because `server.enableStaticServing` is turned on in `.streamlit/config.toml`. `static/marble.png` is a copy of the root `background.png` with the top 90px cropped off to remove a "Made with AI" badge. Pages must not set their own `.stApp` background, or it will cover the image.
- **Session state is the only app state:**
  - `st.session_state.user` holds the raw row tuple returned by the login query in `pages/login.py`: `(id, name, age, address, email, phone, password, role, dob)`. Pages read it by index, so `user[0]` is the id, `user[1]` is the name and `user[7]` is the role. If you change that SELECT, every page that indexes `user` breaks.
  - `st.session_state.cart` is a list of `{id, name, price, quantity, restaurant_id}`. `pages/menu.py` limits the cart to items from one restaurant.
  - `restaurant_id` and `restaurant_name` are set by `pages/home.py` before it switches to `pages/menu.py`.
- **Flow:** home (restaurant list and filter) → menu (add to cart) → cart (checkout inserts into `orders` and `order_items`) → orders (the user's order history). Login and register are separate pages. The admin pages `create_restaurant`, `create_product` and `create_categories` are open only to users whose role is `admin` or `restaurant_owner`.
- **Authorization is checked in the UI only.** Passwords are stored and compared as plaintext.

## Database

- The schema is in `database/create_tables.sql`. Seed data is in `database/insert_*.SQL`; each seed file starts by deleting existing rows and resetting `sqlite_sequence`. Seeds have to be loaded in foreign-key order: users, restaurants, categories, products, then orders.
- `database/database.db` is the live database and is committed alongside the code. It has drifted from the SQL files: it contains a `payments` table that `create_tables.sql` does not define, and more rows than the seed files create.
- Order `status` is one of `pending`, `preparing`, `completed`, `canceled`. `payment_status` is one of `pending`, `paid`, `failed`, `refunded`. User `role` is one of `customer`, `admin`, `restaurant_owner`. These values are enforced by `CHECK` constraints.

## Gotchas

- `pages/create_categories.py` checks the role with `user_data[6]`, which is the password field. Every other page uses `user_data[7]`.
- The `developing-with-streamlit` skill is symlinked into `.claude/skills/` and `.agents/skills/`. Use it for any Streamlit UI or styling work.
