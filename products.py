"""
import snowflake.connector

snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'PUBLIC'
}

try:
    connection = snowflake.connector.connect(**snowflake_config)
    cursor = connection.cursor()

    # Create the table
    cursor.execute 
    CREATE TABLE PRODUCTS (
        id INTEGER,
        title VARCHAR(100),
        price DECIMAL(10, 2),
        description VARCHAR(100000),
        category VARCHAR(100),
        image VARCHAR(500),
        rating DECIMAL(2, 1),
        available INTEGER
    
    
    print("Table created successfully!, ")
    
    cursor.close()
    connection.close()
except Exception as e:
    print("Error:", e)
"""





import snowflake.connector
from flask import Flask, render_template, jsonify, request, json

app = Flask(__name__)

snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'PUBLIC'  
}

connection = snowflake.connector.connect(**snowflake_config)
print("Connected to Snowflake")

def get_products_from_snowflake():
    if connection:
        products_data = []
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM PRODUCTS")
            products_data = cursor.fetchall()  # Fetch all rows from the cursor
            print("THIS IS THE DATA")
        except Exception as e:
            print("Facing exception:", e)
    return products_data

@app.route("/")
def display_products():
    with open(r"C:\Users\1038588\OneDrive - Blue Yonder\program files\Esko\A-sko\Product_Details.json", 'r') as file:
        product_list = json.load(file)
        for product in product_list:
            print(product)
    products_data = get_products_from_snowflake()
    return render_template("products.html", products_data=products_data)

if __name__ == '__main__':
    app.run(debug=True)
