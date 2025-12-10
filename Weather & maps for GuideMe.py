import requests

# ------------------------------
# YOUR API KEYS
# ------------------------------
weather_key = "033a1c3a5d1eac1b1d99b02e0b3de310"
maps_key = "YOUR_GOOGLE_API"
while True:
    start = input("Enter your starting location= ").lower()
    dest = input("Enter your destination= ").lower()
    if start=="antarctica" or dest=="antarctica":
        print("Sorry! We can't help in that")
    else:
        break

# ------------------------------
# STEP 1 — Get Weather Data
# ------------------------------
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={dest}&appid={weather_key}&units=metric"
weather_data = requests.get(weather_url).json()

weather_main = weather_data["weather"][0]["main"].lower()

print("Weather at destination:", weather_main)

# ------------------------------
# STEP 2 — Pick routing mode depending on weather
# ------------------------------
if weather_main in ["rain", "thunderstorm", "snow", "fog"]:
    print("⚠️ Bad weather detected! Fetching SAFER route...")
    alternatives = "true"
else:
    print("✅ Weather is good. Fetching fastest route...")
    alternatives = "false"

# ------------------------------
# STEP 3 — Fetch Route
# ------------------------------
maps_url = (
    f"https://maps.googleapis.com/maps/api/directions/json?"
    f"origin={start}&destination={dest}&alternatives={alternatives}&key={maps_key}"
)

route_data = requests.get(maps_url).json()

# Check if routes exist
if "routes" not in route_data or len(route_data["routes"]) == 0:
    print("❌ No route found! Maybe Google cannot connect between these locations.")
else:
    # Always pick the first (best) recommended route
    route = route_data["routes"][0]["legs"][0]
    print("Distance:", route["distance"]["text"])
    print("Duration:", route["duration"]["text"])
