import requests
api_key = "033a1c3a5d1eac1b1d99b02e0b3de310"
place = input("Enter the place name= ")
url = f"https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}&units=metric"
data = requests.get(url).json()
icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Thunderstorm": "⛈️",
    "Drizzle": "🌦️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Haze": "🌫️",
    "Fog": "🌫️",
}
temp = data["main"]["temp"]
weather_main = data["weather"][0]["main"]
weather_desc = data["weather"][0]["description"]
icon = icons.get(weather_main, "🌍")
print("──────────── Weather Report ────────────")
print(f"📍 Place: {place}")
print(f"🌡 Temperature: {temp}°C")
print(f"{icon} Weather: {weather_desc.capitalize()}")
print("────────────────────────────────────────")
