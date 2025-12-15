# 2.Show Login Form. If login is successful (fake auth if username & passwd issame, consider valid user), 
#   show weather page. There input a city namefrom text box and display current weather information
#   Provide a logoutbutton and on its click, display thanks message.
import streamlit as st
import requests 
import panadas as pd 
import os
from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv("API_KEY")
url = f"https://api.openweathermap.org/data/2.5/weather"

st.title("Weather App")

if"logged_in" not in st.session_state :
    st.session_state.logged_in=False

if "logged_out" not in st.session_state :
    st.session_state.logged_out = False

def login_page():
    st.title ("Login Page :  ")
    username = st.text_input ("Enter Username : ")
    password = st.text_input ("Enter Password : " ,type = "password")
    st.text("Password is username ")

    if st.button(" Login ") :
        if username  and password and username == password :
            st.session_state.logged_in = True
            st.session_state.logged_out = False
            st.success("Login Successful....!")
            st.rerun()
        else :
            st.error("Invalid input (here username and password must be same)")

def weather_page():
    st.header("Weather Information ")
    city = st.text_input("Enter the city name  : ")
    if st.button("Get Weather"):
             if city:
                params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
                }
                response = requests.get(url,params=params)
                if response.status_code == 200 :
                    data = response.json()
                    st.subheader(f"Current weather in {city.title()}")
                    st.write("Temperature : ",data["main"]["temp"])
                    st.write("Weather:", data["weather"][0]["description"].title())
                    st.write("Humidity:", data["main"]["humidity"], "%")
                else :
                    st.error("City not found!")
             else:
                st.warning("Please enter a correct city name")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logged_out = True
        st.rerun()

def thank_you_page():
    st.title("Thank You!")
    st.success("You have been logged out successfully!")


if st.session_state.logged_in:
    weather_page()
elif st.session_state.logged_out:
    thank_you_page()
else:
    login_page()
