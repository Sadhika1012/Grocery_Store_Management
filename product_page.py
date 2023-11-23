import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to the database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='abc123',
            database='store'
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

# Function to create a new product
'''def create_product(name, description, category_id, supplier_id, price, quantity_in_stock):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Product (Name, Description, CategoryID, SupplierID, Price, QuantityInStock) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (name, description, category_id, supplier_id, price, quantity_in_stock))
    connection.commit()
    st.success(f"Product '{name}' created successfully.")

    cursor.close()
    connection.close()'''

def create_product(name, description, category_id, supplier_id, price, quantity_in_stock):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        insert_query = "INSERT INTO Product (Name, Description, CategoryID, SupplierID, Price, QuantityInStock) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, description, category_id, supplier_id, price, quantity_in_stock))
        connection.commit()
        st.success(f"Product '{name}' created successfully.")
    except mysql.connector.Error as e:
        st.error(f"Error creating product: {e}")

    cursor.close()
    connection.close()


# Function to read all products
def read_products():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Product"
    cursor.execute(query)
    products = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return products,column_names

# Function to display products in a table
def display_products_table():
    products,column_names = read_products()
    if products:
        df = pd.DataFrame(products, columns=column_names)
        st.write(df)
    else:
        st.write("No products found.")

# Function to delete a product by ID
def delete_product(product_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Product WHERE ProductID = %s"
    cursor.execute(delete_query, (product_id,))
    connection.commit()
    st.warning(f"Product with ID {product_id} deleted.")

    cursor.close()
    connection.close()

# Function to update product details
def update_product(product_id, name, description, category_id, supplier_id, price, quantity_in_stock):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE Product SET Name = %s, Description = %s, CategoryID = %s, SupplierID = %s, Price = %s, QuantityInStock = %s WHERE ProductID = %s"
    cursor.execute(update_query, (name, description, category_id, supplier_id, price, quantity_in_stock, product_id))
    connection.commit()
    st.success(f"Product with ID {product_id} updated successfully.")

    cursor.close()
    connection.close()


# Function to read all products
def update_products():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Product"
    cursor.execute(query)
    products = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return products

def run():
    st.title("Products")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing products in a table
        display_products_table()

        # Create new product form
        st.write("### Create New Product")
        name = st.text_input("Name")
        description = st.text_area("Description")
        category_id = st.number_input("Category ID")
        supplier_id = st.number_input("Supplier ID")
        price = st.number_input("Price")
        quantity_in_stock = st.number_input("Quantity in Stock")
        if st.button("Create Product"):
            create_product(name, description, category_id, supplier_id, price, quantity_in_stock)

    elif operation == "Update":
        # Display existing products in a table
        display_products_table()

        # Update product form
        st.write("### Update Product")
        products = update_products()
        product_options = {f"{product[1]} (ID: {product[0]})": product[0] for product in products}
        selected_product = st.selectbox("Select Product to Update", list(product_options.keys()))
        product_id = product_options[selected_product]

        updated_name = st.text_input("Updated Name")
        updated_description = st.text_area("Updated Description")
        updated_category_id = st.number_input("Updated Category ID")
        updated_supplier_id = st.number_input("Updated Supplier ID")
        updated_price = st.number_input("Updated Price")
        updated_quantity_in_stock = st.number_input("Updated Quantity in Stock")
        if st.button("Update Product"):
            update_product(product_id, updated_name, updated_description, updated_category_id, updated_supplier_id, updated_price, updated_quantity_in_stock)

    elif operation == "Delete":
        # Display existing products in a table
        display_products_table()

        # Delete product by ID
        st.write("### Delete Product")
        product_id_to_delete = st.number_input("Enter Product ID to delete", min_value=1)
        if st.button("Delete Product"):
            delete_product(product_id_to_delete)

if __name__ == "__main__":
    run()

