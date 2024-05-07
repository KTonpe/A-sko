from flask import Flask, render_template, redirect, url_for, Blueprint, request


snowflake_config = {
    'account': 'vccevuc-sa96036',
    'user': 'keerthanjj',
    'password': 'Mypwsnow123@',
    'database': 'ESKO',
    'schema': 'PUBLIC'
}

order_api = Blueprint("order_api", __name__)
order_api.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
  
@order_api.route('/placeOrder')
def place_order():
    return render_template('placeorder.html')

# @order_api.route('/fetchAddressDetails', methods =['POST'])
# def fetch_address_details():
#     pincode = request.form.get('pincode')
#     return pincode

