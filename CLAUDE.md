# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Talabat-style food delivery app built with Streamlit (pinned in `requirements.txt`) and SQLite. `README.md` explains how it works, how to set it up, and the **Limits** the owner chose. Read the Limits before you "fix" anything, because those trade-offs were made on purpose.

## Running

```bash
streamlit run app.py        # serves on http://localhost:8501
```

Run it from the repo root. Every screen opens `database/database.db` with that relative path and calls `st.switch_page("app_pages/<name>.py")`.

There is no test suite. To check that a change works, use `streamlit.testing.v1.AppTest` from `app.py`: call `at.switch_page("app_pages/x.py").run()` and set `st.session_state.user` to simulate a login. Run it against a **copy** of the project and database, because the screens write to `database/database.db`.

## Architecture

- **`app.py` runs before every page.** It sets the defaults for `user` and `cart`, holds the one shared CSS block, and builds the menu with `st.navigation`. Which pages go into the menu depends on `st.session_state.user["role"]`. A page that isn't in the menu can't be opened at all, so the screens don't check permissions themselves.
- **Screens live in `app_pages/`**, not `pages/`. A `pages/` folder would switch Streamlit back to its old auto-listed sidebar and break the role-based menu.
- **Each screen is self-contained.** It opens its own `sqlite3` connection, runs plain SQL, commits and closes. There is no `services/` layer; the owner chose to keep SQL inline in each screen.
- **The CSS classes `banner` and `card`** are defined once in `app.py` and used by every screen. The background image is `static/marble.png`, which needs `server.enableStaticServing = true` in `.streamlit/config.toml`. Screens must not set their own `.stApp` background, or it will cover the image.
- **Session state:**
  - `user` is `None` or `{"id", "name", "role"}`.
  - `cart` is a list of `{id, name, price, quantity, restaurant_id}`, all from the same restaurant.
  - `restaurant_id` and `restaurant_name` are set by Home before it switches to Menu.
- **After login, call `st.rerun()`**, so `app.py` rebuilds the menu and lands on Home. Don't call `st.switch_page` to a page that isn't in the menu yet. Log out works the same way: `st.session_state.clear()` then `st.rerun()`.

## Database

- **Setup is manual on purpose**, and the app never creates tables. `database/create_tables.sql` is the schema. The `insert_*.SQL` seed files delete their table's rows first and must be loaded in foreign-key order (see README).
- **`CHECK` constraints enforce these values:**
  - order `status`: `pending` / `preparing` / `completed` / `canceled`
  - `payment_status` and `payments.status`: `pending` / `paid` / `failed` / `refunded`
  - `payment_method`: `cash` / `card` / `wallet`
  - `role`: `customer` / `admin` / `restaurant_owner`
- **Turn dates into text with `str()` before saving them.** Python 3.12 deprecates saving `date` objects straight into sqlite3.
- **Order numbers come from the time in milliseconds**, because the column is `UNIQUE`. Seconds clashed when two orders were placed in the same second.

## Kid-simple rules (keep these)

This code is kept simple enough for a curious 12-year-old to read top to bottom.

- Plain variables, `if`s and loops. No classes, decorators, type hints, comprehensions or lambdas. Unpack rows into named variables (`for restaurant_id, name, address, food_type in restaurants:`) instead of indexing them.
- One short comment, in kid words, above anything a kid would ask "why?" about. Constants go at the top in CAPITALS, with a comment saying why.
- Repeating a few lines is fine if it keeps a screen readable on its own.
- Use plain `if` checks with a friendly `st.error` for problems a user will actually hit (empty fields, an email that's already used, not enough stock). Don't add `try`/`except`.
- Use the standard library first. A new library has to do something plain code can't do in about 10 lines, and its version gets pinned in `requirements.txt`.
- Hide what a user can't use (via the menu in `app.py`) instead of showing it and refusing.
- Give each screen one `type="primary"` button for its main action, and use friendly sentence-case labels.
- Every new shortcut that removes safety or capability goes in the README's **Limits** section.
- Use the `developing-with-streamlit` skill (symlinked in `.claude/skills/`) for Streamlit API and styling questions.
