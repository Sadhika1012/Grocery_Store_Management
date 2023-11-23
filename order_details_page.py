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

# Function to create new order details
def create_order_details(order_id, product_id, quantity_ordered, price):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO OrderDetails (OrderID, ProductID, QuantityOrdered, Price) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (order_id, product_id, quantity_ordered, price))
    connection.commit()
    st.success(f"Order details created successfully.")

    cursor.close()
    connection.close()

# Function to read all order details
def read_order_details():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM OrderDetails"
    cursor.execute(query)
    order_details = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return order_details,column_names

# Function to display order details in a table
def display_order_details_table():
    order_details,column_names = read_order_details()
    if order_details:
        df = pd.DataFrame(order_details, columns=column_names)
        st.write(df)
        
    else:
        st.write("No order details found.")

# Function to delete order details by ID
def delete_order_details(order_details_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM OrderDetails WHERE OrderDetailsID = %s"
    cursor.execute(delete_query, (order_details_id,))
    connection.commit()
    st.warning(f"Order details with ID {order_details_id} deleted.")

    cursor.close()
    connection.close()

# Function to update order details
def update_order_details(order_details_id, order_id, product_id, quantity_ordered, price):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE OrderDetails SET OrderID = %s, ProductID = %s, QuantityOrdered = %s, Price = %s WHERE OrderDetailsID = %s"
    cursor.execute(update_query, (order_id, product_id, quantity_ordered, price, order_details_id))
    connection.commit()
    st.success(f"Order details with ID {order_details_id} updated successfully.")

    cursor.close()
    connection.close()

def update_order_detail():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM OrderDetails"
    cursor.execute(query)
    order_details = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return order_details

def run():
    st.title("Order Details")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing order details in a table
        display_order_details_table()

        # Create new order details form
        st.write("### Create New Order Details")
        order_id = st.number_input("Order ID")
        product_id = st.number_input("Product ID")
        quantity_ordered = st.number_input("Quantity Ordered")
        price = st.number_input("Price")
        if st.button("Create Order Details"):
            create_order_details(order_id, product_id, quantity_ordered, price)

    elif operation == "Update":
        # Display existing order details in a table
        display_order_details_table()

        # Update order details form
        st.write("### Update Order Details")
        order_details = update_order_detail()
        order_details_options = {f"Order Details ID: {order_detail[0]}": order_detail[0] for order_detail in order_details}
        selected_order_details = st.selectbox("Select Order Details to Update", list(order_details_options.keys()))
        order_details_id = order_details_options[selected_order_details]

        updated_order_id = st.number_input("Updated Order ID")
        updated_product_id = st.number_input("Updated Product ID")
        updated_quantity_ordered = st.number_input("Updated Quantity Ordered")
        updated_price = st.number_input("Updated Price")
        if st.button("Update Order Details"):
            update_order_details(order_details_id, updated_order_id, updated_product_id, updated_quantity_ordered, updated_price)

    elif operation == "Delete":
        # Display existing order details in a table
        display_order_details_table()

        # Delete order details by ID
        st.write("### Delete Order Details")
        order_details_id_to_delete = st.number_input("Enter Order Details ID to delete", min_value=1)
        if st.button("Delete Order Details"):
            delete_order_details(order_details_id_to_delete)

if __name__ == "__main__":
    run()
