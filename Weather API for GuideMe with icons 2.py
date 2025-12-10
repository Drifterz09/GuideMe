import requests
from colorama import Fore, Style, init
init(autoreset=True)

api_key = "033a1c3a5d1eac1b1d99b02e0b3de310"
city = "Kochi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
data = requests.get(url).json()

temp = data["main"]["temp"]
desc = data["weather"][0]["description"].title()
humidity = data["main"]["humidity"]
wind = data["wind"]["speed"]

# Weather icons
icons = {
    "clear": "☀️",
    "cloud": "☁️",
    "rain": "🌧",
    "storm": "⛈",
    "snow": "❄️",
    "mist": "🌫",
}

# Pick icon based on weather
weather_main = data["weather"][0]["main"].lower()
emoji = "🌍"
for key in icons:
    if key in weather_main:
        emoji = icons[key]

print(Fore.CYAN + "──────────── Weather Report ────────────")
print(Fore.YELLOW + f"📍 City: {city}")
print(Fore.RED + f"🌡 Temperature: {temp}°C")
print(Fore.GREEN + f"🌦 Weather: {emoji} {desc}")
print(Fore.MAGENTA + f"💧 Humidity: {humidity}%")
print(Fore.BLUE + f"💨 Wind Speed: {wind} m/s")
print(Fore.CYAN + "────────────────────────────────────────")
