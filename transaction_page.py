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

# Function to create a new transaction
def create_transaction(order_id, employee_id, transaction_date, transaction_amount):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Transaction (OrderID, EmployeeID, TransactionDate, TransactionAmount) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (order_id, employee_id, transaction_date, transaction_amount))
    connection.commit()
    st.success(f"Transaction created successfully.")

    cursor.close()
    connection.close()

# Function to read all transactions
def read_transactions():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Transaction"
    cursor.execute(query)
    transactions = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return transactions,column_names

# Function to display transactions in a table
def display_transactions_table():
    transactions,column_names = read_transactions()
    if transactions:
        df = pd.DataFrame(transactions, columns=column_names)
        st.write(df)
       
    else:
        st.write("No transactions found.")

# Function to delete a transaction by ID
def delete_transaction(transaction_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Transaction WHERE TransactionID = %s"
    cursor.execute(delete_query, (transaction_id,))
    connection.commit()
    st.warning(f"Transaction with ID {transaction_id} deleted.")

    cursor.close()
    connection.close()

# Function to update transaction details
def update_transaction(transaction_id, order_id, employee_id, transaction_date, transaction_amount):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE Transaction SET OrderID = %s, EmployeeID = %s, TransactionDate = %s, TransactionAmount = %s WHERE TransactionID = %s"
    cursor.execute(update_query, (order_id, employee_id, transaction_date, transaction_amount, transaction_id))
    connection.commit()
    st.success(f"Transaction with ID {transaction_id} updated successfully.")

    cursor.close()
    connection.close()

# Function to read all transactions
def update_transactions():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Transaction"
    cursor.execute(query)
    transactions = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return transactions

def run():
    st.title("Transactions")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Update", "Delete"], index=0)

    if operation == "Create":
        # Display existing transactions in a table
        display_transactions_table()

        # Create new transaction form
        st.write("### Create New Transaction")
        order_id = st.number_input("Order ID")
        employee_id = st.number_input("Employee ID")
        transaction_date = st.date_input("Transaction Date")
        transaction_amount = st.number_input("Transaction Amount")
        if st.button("Create Transaction"):
            create_transaction(order_id, employee_id, transaction_date, transaction_amount)

    elif operation == "Update":
        # Display existing transactions in a table
        display_transactions_table()

        # Update transaction form
        st.write("### Update Transaction")
        transactions = update_transactions()
        transaction_options = {f"Transaction ID: {transaction[0]}": transaction[0] for transaction in transactions}
        selected_transaction = st.selectbox("Select Transaction to Update", list(transaction_options.keys()))
        transaction_id = transaction_options[selected_transaction]

        updated_order_id = st.number_input("Updated Order ID")
        updated_employee_id = st.number_input("Updated Employee ID")
        updated_transaction_date = st.date_input("Updated Transaction Date")
        updated_transaction_amount = st.number_input("Updated Transaction Amount")
        if st.button("Update Transaction"):
            update_transaction(transaction_id, updated_order_id, updated_employee_id, updated_transaction_date, updated_transaction_amount)

    elif operation == "Delete":
        # Display existing transactions in a table
        display_transactions_table()

        # Delete transaction by ID
        st.write("### Delete Transaction")
        transaction_id_to_delete = st.number_input("Enter Transaction ID to delete", min_value=1)
        if st.button("Delete Transaction"):
            delete_transaction(transaction_id_to_delete)

if __name__ == "__main__":
    run()

