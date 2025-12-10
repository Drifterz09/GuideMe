import requests

# -----------------------------
# 🔍 AUTO-CORRECT FUNCTION
# -----------------------------
def google_autocorrect(user_input, maps_key):
    url = (
        "https://maps.googleapis.com/maps/api/place/autocomplete/json?"
        f"input={user_input}&types=(cities)&key={maps_key}"
    )

    data = requests.get(url).json()

    if "predictions" not in data or len(data["predictions"]) == 0:
        return None

    return data["predictions"][0]["description"]


# -----------------------------
# 🔁 SAFE INPUT + CONFIRMATION
# -----------------------------
def get_valid_city(prompt_text, maps_key):
    while True:
        user_city = input(prompt_text).strip()

        suggestion = google_autocorrect(user_city, maps_key)

        if suggestion:
            print(f"✔ Did you mean: {suggestion}? (yes/no)")
            confirm = input("> ").lower()

            if confirm.startswith("y"):
                return suggestion
            else:
                print("❌ Okay, retry...\n")
        else:
            print("❌ No matching city found. Try again.\n")


# -----------------------------
# 🌦 WEATHER FUNCTION
# -----------------------------
def get_weather(city, weather_key):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={weather_key}&units=metric"
    )

    data = requests.get(url).json()

    try:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"{temp}°C, {desc}"
    except:
        return "Weather unavailable"


# -----------------------------
# 🛣 DIRECTIONS FUNCTION
# -----------------------------
def get_route(start, dest, maps_key):
    url = (
        "https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start}&destination={dest}&key={maps_key}"
    )

    data = requests.get(url).json()

    try:
        leg = data["routes"][0]["legs"][0]
        distance = leg["distance"]["text"]
        duration = leg["duration"]["text"]
        return distance, duration
    except:
        return None, None


# -----------------------------
# 🚀 MAIN PROGRAM
# -----------------------------
maps_key = "7GOOGLE_API_KEY"
weather_key = "OPENWEATHER_KEY"

print("\n🌍 Welcome to GuideMe — Smart Route + Weather System\n")

start_city = get_valid_city("Enter starting location: ", maps_key)
dest_city = get_valid_city("Enter destination: ", maps_key)

print("\n⏳ Fetching best route...\n")

distance, duration = get_route(start_city, dest_city, maps_key)

if distance is None:
    print("❌ Route not found! Try different cities.")
else:
    weather_start = get_weather(start_city, weather_key)
    weather_dest = get_weather(dest_city, weather_key)

    print("🚗 Best Route Found:")
    print(f"➡ From: {start_city}")
    print(f"➡ To:   {dest_city}")
    print(f"🛣 Distance: {distance}")
    print(f"⏱ Duration: {duration}")

    print("\n🌦 WEATHER INFO:")
    print(f"{start_city}: {weather_start}")
    print(f"{dest_city}: {weather_dest}")
