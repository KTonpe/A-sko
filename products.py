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
 
 
def get_products(age_category=None):
    products = []
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if age_category:
                if age_category == 'below_10':
                    cursor.execute("SELECT * FROM ESKO.PUBLIC.PRODUCTS WHERE AGE < 10")
                elif age_category == '10_to_20':
                    cursor.execute("SELECT * FROM ESKO.PUBLIC.PRODUCTS WHERE AGE BETWEEN 10 AND 20")
                elif age_category == 'above_20':
                    cursor.execute("SELECT * FROM ESKO.PUBLIC.PRODUCTS WHERE AGE > 20")
                else:
                    cursor.execute("SELECT * FROM ESKO.PUBLIC.PRODUCTS")
            else:
                cursor.execute("SELECT * FROM ESKO.PUBLIC.PRODUCTS")
            products = cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching product data:", e)
        finally:
            cursor.close()
            conn.close()
    return products
 
 
def get_product_by_name(title):
    product = None
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCTS WHERE title = %s", (title,))
            product = cursor.fetchone()
        except Exception as e:
            print("An error occurred while fetching product by title:", e)
        finally:
            cursor.close()
            conn.close()
    return product
 
 
def add_to_cart(title):
    product = get_product_by_name(title)
    if product:
        if 'cart' not in session:
            session['cart'] = []
 
        session['cart'].append(product)
        session.modified = True
        print("Product added to cart:", product)
 
 
def remove_from_cart(title):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item[1] != title]
        session.modified = True
 
 
def get_cart():
    return session.get('cart', [])
 
 
@app.route('/')
def index():
    age_category = request.args.get('age_category')
    products = get_products(age_category)
    return render_template('index.html', products=products)
 
 
@app.route('/product/<string:title>')
def product(title):
    product = get_product_by_name(title)
    return render_template('product.html', product=product)
 
 
@app.route('/add_to_cart/<string:title>', methods=['POST'])
def add_to_cart_route(title):
    add_to_cart(title)
    return redirect(url_for('index'))
 
 
@app.route('/remove_from_cart/<string:title>', methods=['POST'])
def remove_from_cart_route(title):
    remove_from_cart(title)
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
            cursor.execute("SELECT * FROM PRODUCTS WHERE title LIKE %s", ('%' + query + '%',))
            products = cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching product data:", e)
        finally:
            cursor.close()
            conn.close()
    return products
 
 
if __name__ == '__main__':
    app.run(debug=True)