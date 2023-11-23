import streamlit as st
import mysql.connector
import pandas as pd

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='abc123',
            database='store'  # Your database name
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None
 # Assuming database.py contains the get_connection function

def read_categories():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Category"
    cursor.execute(query)
    categories = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return categories,column_names

def display_categories_table():
    categories,column_names = read_categories()
    if categories:
        df = pd.DataFrame(categories, columns=column_names)
        st.write(df)
        
    else:
        st.write("No categories found.")

def create_category(category_name):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Category (CategoryName) VALUES (%s)"
    cursor.execute(insert_query, (category_name,))
    connection.commit()
    st.success(f"Category '{category_name}' created successfully.")

    cursor.close()
    connection.close()

def update_category(category_id, new_name):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE Category SET CategoryName = %s WHERE CategoryID = %s"
    cursor.execute(update_query, (new_name, category_id))
    connection.commit()
    st.success(f"Category with ID {category_id} updated successfully.")

    cursor.close()
    connection.close()

def delete_category(category_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Category WHERE CategoryID = %s"
    cursor.execute(delete_query, (category_id,))
    connection.commit()
    st.warning(f"Category with ID {category_id} deleted.")

    cursor.close()
    connection.close()

def run():
    st.title("Categories")

    # Display existing categories
    display_categories_table()

    # CRUD operations
    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)
    
    if operation == "Create":
        new_category_name = st.text_input("Enter category name")
        if st.button("Create"):
            create_category(new_category_name)

    elif operation == "Update":
        category_id = st.number_input("Enter Category ID to update", min_value=1)
        new_name = st.text_input("Enter new name")
        if st.button("Update"):
            update_category(category_id, new_name)

    elif operation == "Delete":
        category_id = st.number_input("Enter Category ID to delete", min_value=1)
        if st.button("Delete"):
            delete_category(category_id)

if __name__ == "__main__":
    run()
