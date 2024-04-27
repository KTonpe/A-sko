"""
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

    create_table_query = 
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


    conn.cursor().execute(create_table_query)

    with open(r'A-sko/combines_products.json', 'r') as file:
        data = json.load(file)

    insert_query = 
    INSERT INTO products (title, gender, ID, price, available, description, age, rating, image_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    

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

"""





from flask import Flask, render_template, session, redirect, url_for, request
import snowflake.connector

snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'PUBLIC'
}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def get_connection():
    try:
        return snowflake.connector.connect(**snowflake_config)
    except Exception as e:
        print("An error occurred while connecting to Snowflake:", e)
        return None


def get_products():
    products = []
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCTS")
            products = cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching product data:", e)
        finally:
            cursor.close()
            conn.close()
    return products


def get_product_by_name(name):
    product = None
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCTS WHERE NAME = %s", (name,))
            product = cursor.fetchone()
        except Exception as e:
            print("An error occurred while fetching product by name:", e)
        finally:
            cursor.close()
            conn.close()
    return product


def add_to_cart(name):
    product = get_product_by_name(name)
    if product:
        if 'cart' not in session:
            session['cart'] = []

        session['cart'].append(product)
        session.modified = True
        print("Product added to cart:", product)


def remove_from_cart(name):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item[1] != name]
        session.modified = True


def get_cart():
    return session.get('cart', [])


@app.route('/')
def index():
    age_category = request.args.get('age_category')
    products = get_products()
    if age_category:
        if age_category == 'below_10':
            products = [product for product in products if product[6] < 10]
        elif age_category == '10_to_20':
            products = [product for product in products if 10 <= product[6] <= 20]
        elif age_category == 'above_20':
            products = [product for product in products if product[6] > 20]
    return render_template('index.html', products=products)


@app.route('/product/<string:name>')
def product(name):
    product = get_product_by_name(name)
    return render_template('product.html', product=product)


@app.route('/add_to_cart/<string:name>', methods=['POST'])
def add_to_cart_route(name):
    add_to_cart(name)
    return redirect(url_for('index'))


@app.route('/remove_from_cart/<string:name>', methods=['POST'])
def remove_from_cart_route(name):
    remove_from_cart(name)
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_contents = get_cart()
    print("Cart contents:", cart_contents)
    return render_template('cart.html', cart_contents=cart_contents)


@app.route('/search')
def search():
    query = request.args.get('query')
    products = get_products_by_query(query)
    return render_template('index.html', products=products)


def get_products_by_query(query):
    products = []
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCTS WHERE NAME LIKE %s", ('%' + query + '%',))
            products = cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching product data:", e)
        finally:
            cursor.close()
            conn.close()
    return products


if __name__ == '__main__':
    app.run(debug=True)
