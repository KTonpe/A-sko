import snowflake.connector
import json
from config import snowflake_config

with open("new_directory_name\Product_Details.json",'r') as file:
    json_data = json.load(file)



try:
    connection = snowflake.connector.connect(**snowflake_config)
    cursor = connection.cursor()

    # Insert data into the table
    for item in json_data:
        cursor.execute("""
            INSERT INTO PRODUCTS (id, title, price, description, category, image, rating, available)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['id'], item['title'], item['price'], item['description'],
            item['category'], item['image'], item['rating'], item['available']
        ))

    print("Data inserted successfully.")
    connection.commit()  
    cursor.close()
    connection.close()
except Exception as e:
    print("Error:", e)
