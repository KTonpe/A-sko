from flask import Flask, request, jsonify
import snowflake.connector
import json

new_adding_data_from_api = []

snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'ESKO/PUBLIC'
}

app = Flask(__name__)


@app.route('/aboutOfA-sko', methods=['GET'])
def home():
    info = """
                <h1>Welcome to World of A-SKO!</h1>
                <p>Welcome to our A-SKO Fashion Store, where style transcends age! Explore a diverse range of fashion styles for babies, teens, and adults. From trendy teen streetwear to sophisticated adult ensembles, we've got something for everyone. Login to unlock exclusive features and personalized recommendations. Dive into the world of fashion with style guides and trend forecasts. Join us on a stylish adventure where age is just a number, and fashion is timeless.</p> 
            """
    return info

@app.route('/post_data', methods=['POST'])
def post_data():
    new_item = request.json
    new_adding_data_from_api.append(new_item)
    try:
        connection = snowflake.connector.connect(**snowflake_config)
        cursor = connection.cursor()

        for item in new_adding_data_from_api:
            print("Processing item:", item)
            id_value = item.get('ID')  # Corrected 'ID' to 'id'
            print("ID value:", id_value)
            cursor.execute("""
            INSERT INTO PRODUCTS (ID, title, price, description, image, age, available, gender, rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            (
                item.get('ID'), item.get('title'), item.get('price'), item.get('description'), item.get('image_url'),
                item.get('age'), item.get('available'), item.get('gender'), item.get('rating')
            )
                        """)
        print("Data inserted successfully.")
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)