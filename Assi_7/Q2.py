import streamlit as st
from dotenv import load_dotenv
import os
import requests
from langchain.chat_models import init_chat_model

load_dotenv()

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
groq_api_key = os.getenv("Groq_API")

if not weather_api_key or not groq_api_key:
    st.error("API keys not found. Please set OPENWEATHER_API_KEY and GROQ_API_KEY in .env")
    st.stop()

llm = init_chat_model(
    model="gpt-4.1",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

st.set_page_config(page_title="Weather Summary", layout="centered")
st.title("Weather Summary App")

city = st.text_input("Enter city name")

if st.button("Get Weather") and city.strip():
    with st.spinner("Fetching weather data..."):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Weather API error: {e}")
            st.stop()

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    description = data["weather"][0]["description"]
    icon_code = data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

    st.subheader(f" Weather in {city.title()}")
    st.image(icon_url, caption=description.title())
    st.metric(" Temperature (°C)", temperature)
    st.metric(" Humidity (%)", humidity)
    st.metric(" Wind Speed (m/s)", wind_speed)

    prompt = f"""
    The current weather in {city} is:
    - {description}
    - Temperature: {temperature} °C
    - Humidity: {humidity} %
    - Wind Speed: {wind_speed} m/s

    Explain this weather in simple English.
    """

    with st.spinner("Generating explanation..."):
        explanation = llm.invoke(prompt)

    st.subheader("Simple Explanation")
    st.write(getattr(explanation, "content", getattr(explanation, "text", "No response")))

elif city == "":
    st.info("Please enter a city name.") 