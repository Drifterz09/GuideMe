import requests
from fuzzywuzzy import process

weather_key = "YOUR_WEATHER_KEY"
maps_key = "YOUR_GOOGLE_MAPS_KEY"

# A list of common Indian/world cities (add more if you want)
CITY_LIST = [
    "Kochi", "Munnar", "Delhi", "Mumbai", "Chennai", "Bengaluru",
    "Hyderabad", "Kolkata", "Tokyo", "Dubai", "London",
    "New York", "Thrissur", "Guruvayur", "Kozhikode"
]


def get_valid_city(prompt_text):
    """Gets user input, autocorrects, and validates city name"""
    while True:
        user_city = input(prompt_text).strip()

        # Auto-correct the spelling using fuzzy matching
        best_match, score = process.extractOne(user_city, CITY_LIST)

        if score >= 70:  # If similarity is good enough
            print(f"✔ Did you mean: {best_match}? (yes/no)")
            confirm = input("> ").lower()

            if confirm.startswith("y"):
                return best_match
            else:
                print("❌ Okay, try typing again.\n")
        else:
            print("❌ City not recognized. Try again!\n")


def get_weather(city):
    """Fetch weather safely"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        return None

    return data


def get_route(start, dest, bad_weather):
    """Fetch route safely"""
    alternatives = "true" if bad_weather else "false"

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start}&destination={dest}&alternatives={alternatives}&key={maps_key}"
    )

    data = requests.get(url).json()

    if "routes" not in data or len(data["routes"]) == 0:
        return None

    return data["routes"][0]["legs"][0]


# ----------------------------
# MAIN PROGRAM
# ----------------------------

print("\n🌍 Welcome to GuideMe — Smart Route + Weather System\n")

start = get_valid_city("Enter starting location: ")
dest = get_valid_city("Enter destination: ")

# Weather Check
weather_data = get_weather(dest)

if weather_data is None:
    print("❌ Couldn’t fetch weather data. Try again later.")
    exit()

weather_main = weather_data["weather"][0]["main"].lower()
print("Weather at destination:", weather_main)

bad_weather = weather_main in ["rain", "snow", "thunderstorm", "fog"]

if bad_weather:
    print("⚠️ Bad weather detected — using safer route!")
else:
    print("✅ Weather is good — using fastest route!")

# Route Check
route = get_route(start, dest, bad_weather)

if route is None:
    print("❌ Google Maps cannot find a route between these locations!")
    exit()

print("\n──────── ROUTE DETAILS ────────")
print("📍 Distance:", route["distance"]["text"])
print("⏱ Duration:", route["duration"]["text"])
print("────────────────────────────────")
