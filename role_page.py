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

# Function to read all roles from the database
def read_roles():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Role"
    cursor.execute(query)
    roles = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return roles,column_names

# Function to display roles in a table
def display_roles_table():
    roles ,column_names= read_roles()
    if roles:
        
        df = pd.DataFrame(roles, columns=column_names)
        st.write(df)
    else:
        st.write("No roles found.")

# Function to create a new role
def create_role(role_name, role_description):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Role (RoleName, RoleDescription) VALUES (%s, %s)"
    cursor.execute(insert_query, (role_name, role_description))
    connection.commit()
    st.success(f"Role '{role_name}' created successfully.")

    cursor.close()
    connection.close()

# Function to delete a role
def delete_role(role_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Role WHERE RoleID = %s"
    cursor.execute(delete_query, (role_id,))
    connection.commit()
    st.warning(f"Role with ID {role_id} deleted.")

    cursor.close()
    connection.close()
    

def run():
    st.title("Role Management")

    # Display existing roles in a table
    display_roles_table()

    # Create new role form
    st.write("### Create New Role")
    role_name = st.text_input("Role Name")
    role_description = st.text_area("Role Description")
    if st.button("Create Role"):
        create_role(role_name, role_description)

    # Delete role by ID
    st.write("### Delete Role")
    role_id = st.number_input("Enter Role ID to delete", min_value=1)
    if st.button("Delete Role"):
        delete_role(role_id)

if __name__ == "__main__":
    run()
