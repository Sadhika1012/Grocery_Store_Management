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

# Function to create a new customer
def create_customer(name, email, phone_number, address):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Customer (Name, Email, PhoneNumber, Address) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (name, email, phone_number, address))
    connection.commit()
    st.success(f"Customer '{name}' created successfully.")

    cursor.close()
    connection.close()

# Function to read all customers
def read_customers():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Customer"
    cursor.execute(query)
    customers = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return customers,column_names



# Function to display customers in a table with column names as headers
def display_customers_table():
    customers, column_names = read_customers()
    if customers:
        st.write("## Customers Table")
        df = pd.DataFrame(customers, columns=column_names)
        st.write(df)
    else:
        st.write("No customers found.")


# Function to delete a customer by ID
def delete_customer(customer_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Customer WHERE CustomerID = %s"
    cursor.execute(delete_query, (customer_id,))
    connection.commit()
    st.warning(f"Customer with ID {customer_id} deleted.")

    cursor.close()
    connection.close()

# Function to update customer details
def update_customer(customer_id, name, email, phone_number, address):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE Customer SET Name = %s, Email = %s, PhoneNumber = %s, Address = %s WHERE CustomerID = %s"
    cursor.execute(update_query, (name, email, phone_number, address, customer_id))
    connection.commit()
    st.success(f"Customer with ID {customer_id} updated successfully.")

    cursor.close()
    connection.close()

# Function to read all customers
def update_customers():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Customer"
    cursor.execute(query)
    customers = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return customers

def run():
    st.title("Customers")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing customers in a table
        display_customers_table()

        # Create new customer form
        st.write("### Create New Customer")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        address = st.text_input("Address")
        if st.button("Create Customer"):
            create_customer(name, email, phone_number, address)

    elif operation == "Update":
        # Display existing customers in a table
        display_customers_table()

        # Update customer form
        st.write("### Update Customer")
        customers = update_customers()
        customer_options = {f"{customer[1]} (ID: {customer[0]})": customer[0] for customer in customers}
        selected_customer = st.selectbox("Select Customer to Update", list(customer_options.keys()))
        customer_id = customer_options[selected_customer]

        updated_name = st.text_input("Updated Name")
        updated_email = st.text_input("Updated Email")
        updated_phone_number = st.text_input("Updated Phone Number")
        updated_address = st.text_input("Updated Address")
        if st.button("Update Customer"):
            update_customer(customer_id, updated_name, updated_email, updated_phone_number, updated_address)

    elif operation == "Delete":
        # Display existing customers in a table
        display_customers_table()

        # Delete customer by ID
        st.write("### Delete Customer")
        customer_id_to_delete = st.number_input("Enter Customer ID to delete", min_value=1)
        if st.button("Delete Customer"):
            delete_customer(customer_id_to_delete)

if __name__ == "__main__":
    run()

