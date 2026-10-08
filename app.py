import streamlit as st

st.set_page_config(page_title="BYTE.ME", page_icon="images/favicon.png", layout="wide")

# The logo sits at the top of the menu. When the menu is folded away, the small icon shows instead.
st.logo("images/logo.png", size="large", icon_image="images/favicon.png")

# Nobody is logged in and the cart is empty until we say otherwise.
if "user" not in st.session_state:
    st.session_state.user = None
if "cart" not in st.session_state:
    st.session_state.cart = []

# The look of the whole app lives here, so every screen matches.
# The picture is served from the static/ folder (see .streamlit/config.toml).
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("app/static/marble.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: transparent;
    }
    .banner {
        background: linear-gradient(120deg, #e85d04, #f48c06);
        padding: 1.8rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
    }
    .banner h1, .banner p {
        color: white;
        margin: 0;
    }
    .card {
        background: white;
        border: 1px solid #f0dfcc;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.7rem;
    }
    /* The dish photo fills a box of the same size on every card. */
    .dish-photo {
        height: 180px;
        background-size: cover;
        background-position: center;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .no-photo {
        font-size: 4rem;
        text-align: center;
        line-height: 180px;
        background: #fff7ed;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Everyone can look at restaurants and menus.
pages = [
    st.Page("app_pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("app_pages/menu.py", title="Menu", icon="🍔"),
]

user = st.session_state.user

if user is None:
    pages.append(st.Page("app_pages/login.py", title="Log in", icon="🔐"))
    pages.append(st.Page("app_pages/register.py", title="Register", icon="📝"))
else:
    pages.append(st.Page("app_pages/cart.py", title="Cart", icon="🛒"))
    pages.append(st.Page("app_pages/orders.py", title="My orders", icon="📦"))

    # Admins and restaurant owners can also add things and manage orders.
    if user["role"] == "admin" or user["role"] == "restaurant_owner":
        pages.append(st.Page("app_pages/add_restaurant.py", title="Add restaurant", icon="🏪"))
        pages.append(st.Page("app_pages/add_product.py", title="Add product", icon="🍕"))
        pages.append(st.Page("app_pages/add_category.py", title="Add category", icon="🏷️"))
        pages.append(st.Page("app_pages/manage_orders.py", title="Manage orders", icon="📋"))

    pages.append(st.Page("app_pages/logout.py", title="Log out", icon="👋"))

# Only the pages in this list show up in the menu, and only they can be opened.
page = st.navigation(pages)
page.run()
