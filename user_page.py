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

# Function to read all users from the database
def read_users():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM User"
    cursor.execute(query)
    users = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return users,column_names

# Function to display users in a table
def display_users_table():
    users,column_names = read_users()
    if users:
        df = pd.DataFrame(users, columns=column_names)
        st.write(df)
        
    else:
        st.write("No users found.")

# Function to create a new user
def create_user(username, mobile, email, address, role_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO User (Username, Mobile, Email, Address, RoleID) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (username, mobile, email, address, role_id))
    connection.commit()
    st.success(f"User '{username}' created successfully.")

    cursor.close()
    connection.close()

# Function to delete a user
def delete_user(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM User WHERE UserID = %s"
    cursor.execute(delete_query, (user_id,))
    connection.commit()
    st.warning(f"User with ID {user_id} deleted.")

    cursor.close()
    connection.close()

# Function to update user details
def update_user(user_id, username, mobile, email, address, role_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE User SET Username = %s, Mobile = %s, Email = %s, Address = %s, RoleID = %s WHERE UserID = %s"
    cursor.execute(update_query, (username, mobile, email, address, role_id, user_id))
    connection.commit()
    st.success(f"User with ID {user_id} updated successfully.")

    cursor.close()
    connection.close()

# Function to read all users from the database
def update_users():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM User"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return users

def run():
    st.title("Users")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing users in a table
        display_users_table()

        # Create new user form
        st.write("### Create New User")
        username = st.text_input("Username")
        mobile = st.text_input("Mobile")
        email = st.text_input("Email")
        address = st.text_input("Address")
        role_id = st.number_input("Role ID")
        if st.button("Create User"):
            create_user(username, mobile, email, address, role_id)

    elif operation == "Update":
    # Display existing users in a table
        display_users_table()

        # Update user form
        st.write("### Update User")
        users = update_users()
        user_options = {f"{user[1]} (ID: {user[0]})": user[0] for user in users}
    
        if user_options:  # Check if user_options is not empty
            selected_user = st.selectbox("Select User to Update", list(user_options.keys()))
            user_id = user_options[selected_user]

            updated_username = st.text_input("Updated Username")
            updated_mobile = st.text_input("Updated Mobile")
            updated_email = st.text_input("Updated Email")
            updated_address = st.text_input("Updated Address")
            updated_role_id = st.number_input("Updated Role ID")
        if st.button("Update User"):
            update_user(user_id, updated_username, updated_mobile, updated_email, updated_address, updated_role_id)
        else:
            st.write("No users found for updating.")


    elif operation == "Delete":
        # Display existing users in a table
        display_users_table()

        # Delete user by ID
        st.write("### Delete User")
        user_id_to_delete = st.number_input("Enter User ID to delete", min_value=1)
        if st.button("Delete User"):
            delete_user(user_id_to_delete)

if __name__ == "__main__":
    run()
