import os
import json
from flask import Flask, request, jsonify, render_template
from fuzzywuzzy import process

app = Flask(__name__)

# Load scrap prices from JSON file
with open(os.path.join(os.path.dirname(__file__), "scrap_prices.json"), "r", encoding="utf-8") as file:
    scrap_data = json.load(file)

# Convert to dictionary for quick lookup
scrap_dict = {item["Name"].lower(): item for item in scrap_data}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_price", methods=["POST"])
def get_price():
    data = request.json
    material_name = data.get("material", "").lower()

    if not material_name:
        return jsonify({"response": "Please provide a material name."})

    # Find the closest match using fuzzy search
    closest_match, confidence = process.extractOne(material_name, scrap_dict.keys())

    if confidence > 70:  # If match confidence is high enough
        item = scrap_dict[closest_match]
        response_text = f"The price of {item['Name']} is ₹{item['Price']} per {item['Unit']}."
        return jsonify({"response": response_text, "image": item.get("Image URL", "")})
    else:
        return jsonify({"response": "Sorry, I couldn't find that material. Try another one."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
