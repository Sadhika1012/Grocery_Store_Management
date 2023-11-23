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

# Function to create a new supplier
def create_supplier(name, address, phone_number, contact_name, email):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Supplier (Name, Address, PhoneNumber, ContactName, Email) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (name, address, phone_number, contact_name, email))
    connection.commit()
    st.success(f"Supplier '{name}' created successfully.")

    cursor.close()
    connection.close()

# Function to read all suppliers
def read_suppliers():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Supplier"
    cursor.execute(query)
    suppliers = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return suppliers,column_names

# Function to display suppliers in a table
def display_suppliers_table():
    suppliers,column_names = read_suppliers()
    if suppliers:
        df = pd.DataFrame(suppliers, columns=column_names)
        st.write(df)
        
    else:
        st.write("No suppliers found.")

# Function to delete a supplier by ID
def delete_supplier(supplier_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Supplier WHERE SupplierID = %s"
    cursor.execute(delete_query, (supplier_id,))
    connection.commit()
    st.warning(f"Supplier with ID {supplier_id} deleted.")

    cursor.close()
    connection.close()

# Function to update supplier details
def update_supplier(supplier_id, name, address, phone_number, contact_name, email):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE Supplier SET Name = %s, Address = %s, PhoneNumber = %s, ContactName = %s, Email = %s WHERE SupplierID = %s"
    cursor.execute(update_query, (name, address, phone_number, contact_name, email, supplier_id))
    connection.commit()
    st.success(f"Supplier with ID {supplier_id} updated successfully.")

    cursor.close()
    connection.close()

def update_suppliers():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Supplier"
    cursor.execute(query)
    suppliers = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return suppliers

def run():
    st.title("Suppliers")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing suppliers in a table
        display_suppliers_table()

        # Create new supplier form
        st.write("### Create New Supplier")
        name = st.text_input("Name")
        address = st.text_input("Address")
        phone_number = st.text_input("Phone Number")
        contact_name = st.text_input("Contact Name")
        email = st.text_input("Email")
        if st.button("Create Supplier"):
            create_supplier(name, address, phone_number, contact_name, email)

    elif operation == "Update":
        # Display existing suppliers in a table
        display_suppliers_table()

        # Update supplier form
        st.write("### Update Supplier")
        suppliers = update_suppliers()
        supplier_options = {f"{supplier[1]} (ID: {supplier[0]})": supplier[0] for supplier in suppliers}
        selected_supplier = st.selectbox("Select Supplier to Update", list(supplier_options.keys()))
        supplier_id = supplier_options[selected_supplier]

        updated_name = st.text_input("Updated Name")
        updated_address = st.text_input("Updated Address")
        updated_phone_number = st.text_input("Updated Phone Number")
        updated_contact_name = st.text_input("Updated Contact Name")
        updated_email = st.text_input("Updated Email")
        if st.button("Update Supplier"):
            update_supplier(supplier_id, updated_name, updated_address, updated_phone_number, updated_contact_name, updated_email)
        else:
            st.write("No suppliers found for updating.")

    elif operation == "Delete":
        # Display existing suppliers in a table
        display_suppliers_table()

        # Delete supplier by ID
        st.write("### Delete Supplier")
        supplier_id_to_delete = st.number_input("Enter Supplier ID to delete", min_value=1)
        if st.button("Delete Supplier"):
            delete_supplier(supplier_id_to_delete)

if __name__ == "__main__":
    run()

