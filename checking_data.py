# This file is only for to check the code

import snowflake.connector
from flask import Flask, render_template, json

app = Flask(__name__)

# Snowflake connection configuration
snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'PUBLIC'
}

# connect karo 
connection = snowflake.connector.connect(**snowflake_config)
print("Connected to Snowflake")

def get_products_from_snowflake():
    """Fetch products data from Snowflake database."""
    products_data = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM PRODUCTS")
            products_data = cursor.fetchall()
            print("Products fetched from Snowflake")
        except Exception as e:
            print("Error fetching products from Snowflake:", e)
    return products_data

def get_products_from_json():
    """Load products data from JSON file."""
    try:
        with open(r"C:\Users\1038588\OneDrive - Blue Yonder\program files\Esko\A-sko\Product_Details.json", 'r') as file:
            product_list = json.load(file)
            print("Products loaded from JSON file")
            return product_list
    except Exception as e:
        print("Error loading products from JSON file:", e)
        return []

@app.route("/")
def display_products():
    """Render product data from both Snowflake and JSON file."""
    snowflake_products = get_products_from_snowflake()
    json_products = get_products_from_json()
    return render_template("products.html", snowflake_products=snowflake_products, json_products=json_products)

if __name__ == '__main__':
    app.run(debug=True)
