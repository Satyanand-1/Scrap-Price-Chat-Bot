import json
from flask import Flask, request, jsonify, render_template
from fuzzywuzzy import process  # Import fuzzy matching

app = Flask(__name__)

# Load scrap prices from JSON file
with open("scrap_prices.json", "r", encoding="utf-8") as file:
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

    # Find the closest match using fuzzy search
    closest_match, confidence = process.extractOne(material_name, scrap_dict.keys())

    if confidence > 70:  # If match confidence is high enough
        item = scrap_dict[closest_match]
        response_text = f"The price of {item['Name']} is ₹{item['Price']} per {item['Unit']}."
        return jsonify({"response": response_text, "image": item["Image URL"]})
    else:
        return jsonify({"response": "Sorry, I couldn't find that material. Try another one."})

if __name__ == "__main__":
    app.run(debug=True)
