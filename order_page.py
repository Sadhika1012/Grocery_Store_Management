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

# Function to create a new order
'''def create_order(customer_id, order_date, total_price, order_status):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO OrderTable (CustomerID, OrderDate, TotalPrice, OrderStatus) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (customer_id, order_date, total_price, order_status))
    connection.commit()
    st.success(f"Order created successfully.")

    cursor.close()
    connection.close()'''

# Function to create a new order
def create_order(customer_id, order_date, total_price, order_status):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO OrderTable (CustomerID, OrderDate, TotalPrice, OrderStatus) VALUES (%s, %s, %s, %s)"
    
    try:
        cursor.execute(insert_query, (customer_id, order_date, total_price, order_status))
        connection.commit()
        st.success("Order created successfully.")
    except mysql.connector.Error as e:
        st.warning(f"Failed to create order: {e.msg}")

    cursor.close()
    connection.close()


# Function to read all orders
def read_orders():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM OrderTable"
    cursor.execute(query)
    orders = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return orders,column_names

# Function to display orders in a table
def display_orders_table():
    orders,column_names = read_orders()
    if orders:
        df = pd.DataFrame(orders, columns=column_names)
        st.write(df)
        
    else:
        st.write("No orders found.")

# Function to delete an order by ID
def delete_order(order_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM OrderTable WHERE OrderID = %s"
    cursor.execute(delete_query, (order_id,))
    connection.commit()
    st.warning(f"Order with ID {order_id} deleted.")

    cursor.close()
    connection.close()

# Function to update order details
def update_order(order_id, customer_id, order_date, total_price, order_status):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE OrderTable SET CustomerID = %s, OrderDate = %s, TotalPrice = %s, OrderStatus = %s WHERE OrderID = %s"
    cursor.execute(update_query, (customer_id, order_date, total_price, order_status, order_id))
    connection.commit()
    st.success(f"Order with ID {order_id} updated successfully.")

    cursor.close()
    connection.close()

# Function to read all orders
def update_orders():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM OrderTable"
    cursor.execute(query)
    orders = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return orders

def run():
    st.title("Orders")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing orders in a table
        display_orders_table()

        # Create new order form
        st.write("### Create New Order")
        customer_id = st.number_input("Customer ID")
        order_date = st.date_input("Order Date")
        total_price = st.number_input("Total Price")
        order_status = st.text_input("Order Status")
        if st.button("Create Order"):
            create_order(customer_id, order_date, total_price, order_status)

    elif operation == "Update":
        # Display existing orders in a table
        display_orders_table()

        # Update order form
        st.write("### Update Order")
        orders = update_orders()
        order_options = {f"Order ID: {order[0]}": order[0] for order in orders}
        selected_order = st.selectbox("Select Order to Update", list(order_options.keys()))
        order_id = order_options[selected_order]

        updated_customer_id = st.number_input("Updated Customer ID")
        updated_order_date = st.date_input("Updated Order Date")
        updated_total_price = st.number_input("Updated Total Price")
        updated_order_status = st.text_input("Updated Order Status")
        if st.button("Update Order"):
            update_order(order_id, updated_customer_id, updated_order_date, updated_total_price, updated_order_status)

    elif operation == "Delete":
        # Display existing orders in a table
        display_orders_table()

        # Delete order by ID
        st.write("### Delete Order")
        order_id_to_delete = st.number_input("Enter Order ID to delete", min_value=1)
        if st.button("Delete Order"):
            delete_order(order_id_to_delete)

if __name__ == "__main__":
    run()
