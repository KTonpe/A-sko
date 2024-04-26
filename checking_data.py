import snowflake.connector
import json

snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'PUBLIC'  
}

try:
    conn = snowflake.connector.connect(
        user=snowflake_config['user'],
        password=snowflake_config['password'],
        account=snowflake_config['account'],
        database=snowflake_config['database'],
        schema=snowflake_config['schema']
    )

    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        title VARCHAR,
        gender VARCHAR,
        ID VARCHAR,
        price FLOAT,
        available INT,
        description VARCHAR,
        age INT,
        rating FLOAT,
        image VARCHAR
    )
    """

    conn.cursor().execute(create_table_query)

    with open(r'A-sko/combines_products.json', 'r') as file:
        data = json.load(file)

    insert_query = """
    INSERT INTO products (title, gender, ID, price, available, description, age, rating, image_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for item in data:
        try:
            image_url = item['image']
        except KeyError:
            print("Error: 'image' key is missing in an item:", item)
            continue  # Skip this item and proceed with the next one

        values = (
            item['title'],
            item['gender'],
            item['ID'],
            item['price'],
            item['available'],
            item['description'],
            item['age'],
            item['rating'],
            image_url
        )
        conn.cursor().execute(insert_query, values)

    conn.commit()
    print("Data inserted successfully!")

except snowflake.connector.Error as e:
    print("Snowflake Error:", e)

finally:
    if 'conn' in locals() and conn is not None:
        conn.close()






