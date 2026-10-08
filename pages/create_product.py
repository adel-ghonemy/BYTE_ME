import streamlit as st
from ui import set_background
import sqlite3
import time


st.set_page_config(page_title="create product", page_icon="📝", layout="wide")

set_background()



if st.session_state.user :
    user_data = st.session_state.user
    st.write(user_data[7])
    
    if user_data[7] == "admin" or user_data[7] == "restaurant_owner":

            st.markdown(
                """
                <style>
                .hero-box {
                    background: linear-gradient(135deg, #f97316 0%, #ef4444 100%);
                    padding: 2rem;
                    border-radius: 1rem;
                    color: white;
                    margin-bottom: 1.5rem;
                }
                .feature-card {
                    background: #ffffff;
                    padding: 1rem;
                    border-radius: 0.9rem;
                    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
                    height: 100%;
                }
                .brand-pill {
                    display: inline-block;
                    background: #fff7ed;
                    color: #c2410c;
                    padding: 0.3rem 0.65rem;
                    border-radius: 999px;
                    font-size: 0.86rem;
                    margin-right: 0.4rem;
                    margin-top: 0.3rem;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="hero-box">
                    <h1 style="margin-bottom: 0.3rem;">create product</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )


            st.write("")

            col1, col2 = st.columns(2)


            with col1:

                name = st.text_input("Name")
                category_id = st.number_input("enter your category_id")
                restaurant_id = st.number_input("enter your restaurant_id")
                calories = st.number_input("enter your calories")
                price = st.number_input("enter your price")   

            with col2:
                rating = st.number_input("enter your rating")
                description = st.text_area("enter your description")
                image_url = st.text_input("enter your image url")
                stock = st.number_input("enter your stock")
                is_available = st.selectbox("is available?", ["1", "0"])





            col3, col4 = st.columns([1, 1])



            with col3:


                if st.button("create", use_container_width=True):
                    if name and category_id and restaurant_id  and calories  and price and rating and description and image_url and stock and is_available:
                        
                        
                        conn = sqlite3.connect('database/database.db')
                        
                        c = conn.cursor()
                        
                        c.execute("INSERT INTO products(name , category_id , restaurant_id  , calories  , price , rating , description , image_url , stock , is_available) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (name , category_id , restaurant_id  , calories  , price , rating , description , image_url , stock , is_available))
                        
                        conn.commit()
                        conn.close()
                        
                        st.success("created successfully!")

                        time.sleep(2)
                        st.switch_page("pages/home.py")
                        
                    else:
                        st.error("Please fill in all the fields.")



            with col4:
                if st.button("Back to Home", use_container_width=True):
                    st.switch_page("pages/home.py")
                    

    else:
        st.error("user does not have permission")  
    
else:
    st.write("user not found")
    st.stop()        