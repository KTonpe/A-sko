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
    cursor.execute(""" 
    CREATE TABLE PRODUCTS (
        id INTEGER,
        title VARCHAR(100),
        price DECIMAL(10, 2),
        description VARCHAR(100000),
        category VARCHAR(100),
        image VARCHAR(500),
        rating DECIMAL(2, 1),
        available INTEGER
    )""")
    
    print("Table created successfully!, ")
    
    cursor.close()
    connection.close()
except Exception as e:
    print("Error:", e)
