import sqlite3
from datetime import datetime

# Connect to the new database (or create it)
conn = sqlite3.connect('MYCART.db')
print(f"Connected to database: {conn}")

# Create a cursor object
cursor = conn.cursor()

# Create the CUSTOMERS table
customer_table = f"""
    CREATE TABLE IF NOT EXISTS CUSTOMERS (
        CUS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CUS_NAME VARCHAR(25),
        CUS_AGE INT,
        CUS_MOB VARCHAR(25)
    )
"""
cursor.execute(customer_table)

# Create the PRODUCTS table
try:
    product_table = f"""
        CREATE TABLE IF NOT EXISTS PRODUCTS (
            PROD_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            PROD_NAME VARCHAR(25),
            PROD_PRICE INT,
            PROD_DESC TEXT
        )
    """
    cursor.execute(product_table)
    conn.commit()
except Exception as e:
    print(e)

# Create the CART table
try:
    cart_table = f"""
        CREATE TABLE IF NOT EXISTS CART (
            CART_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CUS_ID INTEGER,
            PROD_ID INTEGER,
            QUANTITY INT,
            FOREIGN KEY (CUS_ID) REFERENCES CUSTOMERS (CUS_ID),
            FOREIGN KEY (PROD_ID) REFERENCES PRODUCTS (PROD_ID)
        )
    """
    cursor.execute(cart_table)
    conn.commit()
except Exception as e:
    print(f"An error occurred while creating the CART table: {e}")

# Create the MY_ORDERS table
try:
    orders_table = f"""
        CREATE TABLE IF NOT EXISTS MY_ORDERS (
            ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CUS_ID INTEGER,
            PROD_ID INTEGER,
            ORDER_DATE TEXT,
            QUANTITY INT,
            TOTAL_PRICE INT,
            FOREIGN KEY (CUS_ID) REFERENCES CUSTOMERS (CUS_ID),
            FOREIGN KEY (PROD_ID) REFERENCES PRODUCTS (PROD_ID)
        )
    """
    cursor.execute(orders_table)
    conn.commit()
except Exception as e:
    print(f"An error occurred while creating the MY_ORDERS table: {e}")

# Function to create a customer
def create_customer():
    try:
        cus_name = input("Enter Your Name: ")
        cus_age = int(input("Enter Your Age: "))
        cus_mob = input("Enter Your Mobile: ")
        insert_cus = f""" INSERT INTO CUSTOMERS (CUS_NAME, CUS_AGE, CUS_MOB) VALUES('{cus_name}', '{cus_age}', '{cus_mob}'); """
        cursor.execute(insert_cus)
        conn.commit()
        print("Customer Created.")
    except Exception as e:
        print(e)

# Function to add products
def add_products():
    try:
        prod_name = input("Enter Product Name: ")
        prod_price = int(input("Enter Product Price: "))
        prod_desc = input("Enter Product Description: ")
        insert_prod = f""" INSERT INTO PRODUCTS (PROD_NAME, PROD_PRICE, PROD_DESC) VALUES('{prod_name}', '{prod_price}', '{prod_desc}'); """
        cursor.execute(insert_prod)
        conn.commit()
        print("Product Added.")
    except Exception as e:
        print(e)

# Function to add items to cart
def add_to_cart():
    try:
        cus_id = int(input("Enter Customer ID: "))
        prod_id = int(input("Enter Product ID: "))
        qty = int(input("Enter Quantity: "))
        insert_cart = f""" INSERT INTO CART (CUS_ID, PROD_ID, QUANTITY) VALUES('{cus_id}', '{prod_id}', '{qty}'); """
        cursor.execute(insert_cart)
        conn.commit()
        print("Product Added to Cart.")
    except Exception as e:
        print(e)

# Function to show cart
def show_cart():
    query = """
    SELECT CART.CART_ID, CUSTOMERS.CUS_NAME, PRODUCTS.PROD_NAME, CART.QUANTITY, PRODUCTS.PROD_PRICE
    FROM CART
    JOIN CUSTOMERS ON CART.CUS_ID = CUSTOMERS.CUS_ID
    JOIN PRODUCTS ON CART.PROD_ID = PRODUCTS.PROD_ID
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            cart_id, customer_name, product_name, quantity, price = row
            print(f"Cart ID: {cart_id}, Customer: {customer_name}, Product: {product_name}, Quantity: {quantity}, Total Price: {quantity * price}")
    else:
        print("Cart is empty.")

# Function to show orders
def show_orders():
    query = """
    SELECT MY_ORDERS.ORDER_ID, CUSTOMERS.CUS_NAME, PRODUCTS.PROD_NAME, MY_ORDERS.QUANTITY, MY_ORDERS.TOTAL_PRICE, MY_ORDERS.ORDER_DATE
    FROM MY_ORDERS
    JOIN CUSTOMERS ON MY_ORDERS.CUS_ID = CUSTOMERS.CUS_ID
    JOIN PRODUCTS ON MY_ORDERS.PROD_ID = PRODUCTS.PROD_ID
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    shipment_data = datetime(2024, 7, 28, 18, 18, 0)
    current_time = datetime.now()

    if rows:
        for row in rows:
            order_id, customer_name, product_name, quantity, total_price, order_date = row
            if shipment_data > current_time:
                print(f"Order ID: {order_id}, Customer: {customer_name}, Product: {product_name}, Quantity: {quantity}, Total Price: {total_price}, Order Date: {order_date}, Shipped on: {shipment_data}")
            else:
                print(f"Order ID: {order_id}, Customer: {customer_name}, Product: {product_name}, Quantity: {quantity}, Total Price: {total_price}, Order Date: {order_date}, Shipped on: Not shipped yet")
    else:
        print("No orders found.")

# Function to make an order
def make_order():
    try:
        cus_id = int(input("Enter Customer ID: "))
        prod_id = int(input("Enter Product ID: "))
        qty = int(input("Enter Quantity: "))
        
        # Get the product price
        cursor.execute("SELECT PROD_PRICE FROM PRODUCTS WHERE PROD_ID = ?", (prod_id,))
        prod_price = cursor.fetchone()
        
        if not prod_price:
            print(f"Product ID {prod_id} does not exist.")
            return
        
        # Calculate the total price
        total_price = prod_price[0] * qty
        
        # Get the current date
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert the order into MY_ORDERS table
        cursor.execute("INSERT INTO MY_ORDERS (CUS_ID, PROD_ID, ORDER_DATE, QUANTITY, TOTAL_PRICE) VALUES (?, ?, ?, ?, ?)", 
                       (cus_id, prod_id, order_date, qty, total_price))
        
        conn.commit()
        print("Order made successfully.")
    except Exception as e:
        print(f"An error occurred while making the order: {e}")


