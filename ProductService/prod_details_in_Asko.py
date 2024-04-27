from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Dummy data to store posted items
data = []
file_path = "A-sko\Product_Details.json"

# Route to handle POST requests
@app.route('/', methods=['GET'])
def home():
    info = "<h1>Welcome to World of Apprentice in BlueYonder!</h1>"
    return info



@app.route('/post_data', methods=['POST'])
def post_data():
    # Get JSON data from the request
    new_item = request.json

    # Append the new item to the data list
    data.append(new_item)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    # Return a success message along with the posted data
    return jsonify({"message": "Data posted successfully", "data": new_item}), 201

if __name__ == '__main__':
    app.run(debug=True)
