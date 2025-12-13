#  Create a weather app that takes city input and displays forecast

import requests

api_key="60ab20a9dd3f01c2d194334ff692f253"
city = input("Enter the city : ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)

print ("Status :",response.status_code)
weather = response.json()
# print(weather)
print("\nTemperature: ", weather["main"]["temp"])
print ("Humidity : ", weather["main"]["humidity"])
print ("Wind speed : ", weather["wind"]["speed"])
print ("Sunset : ", weather["sys"]["sunset"])
print ("Sunrise : ", weather["sys"]["sunrise"])