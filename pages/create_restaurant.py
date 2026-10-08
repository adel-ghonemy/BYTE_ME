import streamlit as st
from ui import set_background
import sqlite3
import time


st.set_page_config(page_title="create restaurant", page_icon="📝", layout="wide")

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
                <h1 style="margin-bottom: 0.3rem;">create restaurant</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )


        st.write("")

        col1, col2 = st.columns(2)


        with col1:

            name = st.text_input("Name")
            opendate = st.date_input("enter your date")

            

        with col2:
            phone = st.text_input("Phone Number")
            type = st.text_input("enter the type")



        address = st.text_input("Address")

        col3, col4 = st.columns([1, 1])



        with col3:


            if st.button("create", use_container_width=True):
                if name and opendate and address  and phone  and type:
                    
                    
                    conn = sqlite3.connect('database/database.db')
                    
                    c = conn.cursor()
                    
                    c.execute("INSERT INTO restaurant(name, opendate, address, phone, type) VALUES (?, ?, ?, ?, ?)",
                            (name,opendate , address , phone, type))
                    
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