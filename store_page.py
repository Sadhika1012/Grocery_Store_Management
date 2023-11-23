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

# Function to create a new store
def create_store(description, store_type, manager_id, phone_number, address):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Store (Description, Type, Manager, PhoneNumber, Address) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (description, store_type, manager_id, phone_number, address))
    connection.commit()
    st.success(f"Store '{description}' created successfully.")

    cursor.close()
    connection.close()

# Function to read all stores
def read_stores():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Store"
    cursor.execute(query)
    stores = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return stores,column_names

# Function to display stores in a table
def display_stores_table():
    stores,column_names = read_stores()
    if stores:
        
        df = pd.DataFrame(stores, columns=column_names)
        st.write(df)
    else:
        st.write("No stores found.")

# Function to delete a store by ID
def delete_store(store_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Store WHERE StoreID = %s"
    cursor.execute(delete_query, (store_id,))
    connection.commit()
    st.warning(f"Store with ID {store_id} deleted.")

    cursor.close()
    connection.close()

# Function to update store details
def update_store(store_id, description, store_type, manager_id, phone_number, address):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE Store SET Description = %s, Type = %s, Manager = %s, PhoneNumber = %s, Address = %s WHERE StoreID = %s"
    cursor.execute(update_query, (description, store_type, manager_id, phone_number, address, store_id))
    connection.commit()
    st.success(f"Store with ID {store_id} updated successfully.")

    cursor.close()
    connection.close()

# Function to read all stores
def update_stores():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Store"
    cursor.execute(query)
    stores = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return stores

def run():
    st.title("Store")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing stores in a table
        display_stores_table()

        # Create new store form
        st.write("### Create New Store")
        description = st.text_input("Description")
        store_type = st.text_input("Type")
        manager_id = st.number_input("Manager ID")
        phone_number = st.text_input("Phone Number")
        address = st.text_input("Address")
        if st.button("Create Store"):
            create_store(description, store_type, manager_id, phone_number, address)

    elif operation == "Update":
        # Display existing stores in a table
        display_stores_table()

        # Update store form
        st.write("### Update Store")
        stores = update_stores()
        store_options = {f"{store[1]} (ID: {store[0]})": store[0] for store in stores}
        selected_store = st.selectbox("Select Store to Update", list(store_options.keys()))
        store_id = store_options[selected_store]

        updated_description = st.text_input("Updated Description")
        updated_store_type = st.text_input("Updated Type")
        updated_manager_id = st.number_input("Updated Manager ID")
        updated_phone_number = st.text_input("Updated Phone Number")
        updated_address = st.text_input("Updated Address")
        if st.button("Update Store"):
            update_store(store_id, updated_description, updated_store_type, updated_manager_id, updated_phone_number, updated_address)

    elif operation == "Delete":
        # Display existing stores in a table
        display_stores_table()

        # Delete store by ID
        st.write("### Delete Store")
        store_id_to_delete = st.number_input("Enter Store ID to delete", min_value=1)
        if st.button("Delete Store"):
            delete_store(store_id_to_delete)

if __name__ == "__main__":
    run()
