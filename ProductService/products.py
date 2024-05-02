from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import snowflake.connector

snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'PUBLIC'
}

products_api = Blueprint('products_api', __name__)
products_api.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def get_connection():
    try:
        return snowflake.connector.connect(**snowflake_config)
    except Exception as e:
        print("An error occurred while connecting to Snowflake:", e)
        return None


def get_products(age_category=None, page=1, per_page=10):
    products = []
    total_count = 0
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM ESKO.PUBLIC.PRODUCTS"
            if age_category:
                if age_category == 'below_10':
                    query += " WHERE AGE < 10"
                elif age_category == '10_to_20':
                    query += " WHERE AGE BETWEEN 10 AND 20"
                elif age_category == 'above_20':
                    query += " WHERE AGE > 20"
            cursor.execute(query)
            total_products = cursor.fetchall()
            total_count = len(total_products)
            products = total_products[(page - 1) * per_page: page * per_page]
        except Exception as e:
            print("An error occurred while fetching product data:", e)
        finally:
            cursor.close()
            conn.close()
    return products, total_count


def get_product_by_name(title):
    product = None
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PUBLIC.PRODUCTS WHERE title = %s", (title,))
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

        # Check if the product is already in the cart
        for item in session['cart']:
            item[9] = 1
            if item[1] == title:
                # If it is, increment the quantity and exit the function
                item[9] += 1
                session.modified = True
                print("Product quantity increased in cart:", title)
                return

        # If the product is not in the cart, add it with a quantity of 1
        product_with_quantity = list(product)
        product_with_quantity.append(1)  # Quantity of the product
        session['cart'].append(product_with_quantity)
        session.modified = True
        print("Product added to cart:", title)



def remove_from_cart(title):
    if 'cart' in session:
        cart = session['cart']
        for i, item in enumerate(cart):
            if item[1] == title:
                if item[9] > 1:
                    item[9] -= 1
                else:  
                    # If quantity is already 0 or less, remove the item from the cart
                    del cart[i]
                    break  # Exit the loop after removing one instance of the product
        session['cart'] = cart  # Update the cart in the session
        session.modified = True  # Mark the session as modified






def get_cart():
    return session.get('cart', [])


@products_api.route('/displayProducts')
def index():
    page = request.args.get('page', default=1, type=int)
    age_category = request.args.get('age_category')  # Retrieve age category from query parameters
    products, total_count = get_products(age_category=age_category, page=page)
    per_page = 10  # Number of products per page
    total_pages = (total_count + per_page - 1) // per_page
    return render_template('index.html', products=products, page=page, total_pages=total_pages)


@products_api.route('/product/<string:title>')
def product(title):
    product = get_product_by_name(title)
    return render_template('product.html', product=product)


@products_api.route('/add_to_cart/<string:title>', methods=['POST'])
def add_to_cart_route(title):
    add_to_cart(title)
    return redirect(url_for('.index'))


@products_api.route('/remove_from_cart/<string:title>', methods=['POST'])
def remove_from_cart_route(title):
    remove_from_cart(title)
    return redirect(url_for('.cart'))


@products_api.route('/cart')
def cart():
    cart_contents = get_cart()
    print("Cart contents:", cart_contents)
    return render_template('cart.html', cart_contents=cart_contents)


@products_api.route('/search')
def search():
    query = request.args.get('query')
    products = get_products_by_query(query)
    page = request.args.get("page", type=int, default=1)
    per_page = 10  # Assuming 10 products per page
    total_count = len(products)
    total_pages = (total_count + per_page - 1) // per_page
    return render_template('index.html', page=page, products=products, total_pages=total_pages)



def get_products_by_query(query):
    products = []
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PUBLIC.PRODUCTS WHERE title LIKE %s", ('%' + query + '%',))
            products = cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching product data:", e)
        finally:
            cursor.close()
            conn.close()
    return products


@products_api.route('/orderdetails')
def order_details():
    return render_template('orderdetails.html')
#ehen i click on the add cart button in cart bagged para increased by one based on clickings also , remove from cart clicken it should be decremented by one based on clickings and availability
