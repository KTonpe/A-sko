
# check the code before going 




























"""

import snowflake.connector
import json

snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'ESKO/PUBLIC'
}

with open(r"C:\Users\1038588\OneDrive - Blue Yonder\program files\A-sko\A-sko\combines_products.json", 'r') as file:
    json_data = json.load(file)

try:
    connection = snowflake.connector.connect(**snowflake_config)
    cursor = connection.cursor()
    for item in json_data:
        print("Processing item:", item)
        id_value = item.get('ID')  # Corrected 'ID' to 'id'
        print("ID value:", id_value)
        cursor.execute(
        INSERT INTO PRODUCTS (ID, title, price, description, image, age, available, gender, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
         (
            id_value, item.get('title'), item.get('price'), item.get('description'), item.get('image_url'),
            item.get('age'), item.get('available'), item.get('gender'), item.get('rating')
        ))  
    print("Data inserted successfully.")
    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print("Error:", e)


 
 Insert data into the table
for item in json_data:
        print("Processing item:", item)
        id_value = item.get('ID')
        print("ID value:", id_value)
        cursor.execute(
        INSERT INTO PRODUCTS (id, title, price, description, image_url, age, available, gender, gender, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    , (
        item.get('ID'), item.get('title'), item.get('price'), item.get('description'), item.get('image_url'), item.get('age'), item.get('available', item.get('gender'), item.get('rating'))
    ))

 
  Insert data into the table
for item in json_data:
        print("Processing item:", item)
        id_value = item.get('ID')
        print("ID value:", id_value)
        cursor.execute(
        INSERT INTO PRODUCTS (id, title, price, description, image_url, age, available, gender, gender, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    , (
        item.get('ID'), item.get('title'), item.get('price'), item.get('description'), item.get('image_url'), item.get('age'), item.get('available', item.get('gender'), item.get('rating'))
    ))
"""