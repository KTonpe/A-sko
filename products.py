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

def get_products():
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
            SELECT * FROM PRODUCTS""")
            print("Data renderd successfully")
            return cursor.fetchall()
        except:
            print("No data found")
            

@app.route("/")
def display_products():
    products_data = get_products()
    return render_template("products.html", products_data = products_data)

if __name__ == '__main__':
    app.run(debug=True)
