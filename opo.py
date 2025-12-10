from flask import Flask, request, jsonify

app = Flask(__name__)

# ------------------ API KEYS ------------------
MAPBOX_API_KEY = "YOUR_MAPBOX_KEY"

# ------------------ CHECKLIST DATA ------------------
def get_checklist(place_type):
    checklists = {
        "beach": ["Swimsuit", "Sunscreen", "Beach Towel", "Sunglasses",
                  "Flip Flops", "Hat/Cap", "Water Bottle", "Snacks",
                  "Portable Charger"],

        "mountain": ["Hiking Boots", "Warm Jacket", "Gloves", "Map/Compass",
                     "Flashlight", "First Aid Kit", "Water Bottle",
                     "Energy Bars", "Backpack"],

        "city": ["Comfortable Shoes", "ID/Passport", "Wallet/Cash",
                 "Phone + Charger", "Power Bank", "Travel Guide/Map",
                 "Reusable Water Bottle", "Camera", "Light Jacket"],

        "desert": ["Sunscreen", "Hat/Bandana", "Light Clothing",
                   "Extra Water", "Sunglasses", "Snacks", "Lip Balm",
                   "Sturdy Shoes", "Portable Fan (optional)"],
    }

    return checklists.get(place_type.lower(), ["Basic Clothing", "Water Bottle", "Phone + Charger"])

# ------------------ MAP LOOKUP ------------------
def get_map_url(city):
    # Returns a PNG static map URL
    return (
        f"https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/"
        f"{city.replace(' ', '%20')},4,0/600x400"
        f"?access_token={MAPBOX_API_KEY}&format=png"
    )

# -----------------------------------------------------
#                API ROUTES
# -----------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "GuideMe API": "Working!",
        "endpoints": {
            "/checklist?type=beach": "Get checklist",
            "/map?city=Tokyo": "Get static map URL",
            "/all?type=beach&city=Dubai": "Get everything combined"
        }
    })

@app.route("/checklist")
def checklist():
    place_type = request.args.get("type", "")
    return jsonify({
        "destination_type": place_type,
        "checklist": get_checklist(place_type)
    })

@app.route("/map")
def map_api():
    city = request.args.get("city", "")
    return jsonify({
        "city": city,
        "map_url": get_map_url(city)
    })

@app.route("/all")
def all_data():
    place_type = request.args.get("type", "")
    city = request.args.get("city", "")

    return jsonify({
        "destination_type": place_type,
        "city": city,
        "checklist": get_checklist(place_type),
        "map_url": get_map_url(city)
    })

# -----------------------------------------------------
#                RUN SERVER
# -----------------------------------------------------

if __name__ == "__main__":
    print("GuideMe API running at http://127.0.0.1:5000")
    app.run(debug=True)
