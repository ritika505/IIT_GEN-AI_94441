from weather import get_weather

city = input("Enter city name: ")

weather = get_weather(city)

if weather:
    print("Temperature :", weather["main"]["temp"], "°C")
    print("Humidity    :", weather["main"]["humidity"], "%")
    print("Wind speed  :", weather["wind"]["speed"], "m/s")
    print("Sunrise     :", weather["sys"]["sunrise"])
    print("Sunset      :", weather["sys"]["sunset"])
else:
    print("City not found or API error")
