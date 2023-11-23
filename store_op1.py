import mysql.connector
import streamlit as st

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


# Function to fetch customer order history
def customer_order_history(customer_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM OrderTable WHERE CustomerID = %s"
    cursor.execute(query, (customer_id,))
    orders = cursor.fetchall()

    cursor.close()
    connection.close()

    return orders

def calculate_average_price_by_category(category_name):
    connection = connect_to_db()
    cursor = connection.cursor()

    # Nested query to calculate average price of products in a specific category
    query = f"""
    SELECT AVG(Price) 
    FROM Product 
    WHERE CategoryID = (
        SELECT CategoryID 
        FROM Category 
        WHERE CategoryName = %s
    )
    """
    cursor.execute(query, (category_name,))
    average_price = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return average_price



# Function to get total transactions by employee
def get_total_transactions_by_employee(employee_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        query = f"SELECT GetEmployeeTransactionInfo({employee_id})"
        cursor.execute(query)
        total_transactions = cursor.fetchone()[0]
        st.write(f"Total transactions for Employee ID {employee_id}: {total_transactions}")
    except mysql.connector.Error as e:
        st.error(f"Error fetching total transactions: {e}")

    cursor.close()
    connection.close()


# Function to retrieve low stock notifications
def get_low_stock_notifications(product_id, threshold_quantity):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute(f"CALL NotifyLowStock({product_id}, {threshold_quantity})")
        result = cursor.fetchone()
        st.write(result)  # Printing the low stock notification
    except mysql.connector.Error as e:
        st.error(f"Error fetching low stock notifications: {e}")

    cursor.close()
    connection.close()

# Function to get employees by date of birth
def get_employees_by_dob(date_of_birth):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        query = "CALL GetEmployeesByDOB(%s)"
        cursor.execute(query, (date_of_birth,))
        employees = cursor.fetchall()
        
        for employee in employees:
            st.table(employee)  # Display employee information

    except mysql.connector.Error as e:
        st.error(f"Error fetching employees by date of birth: {e}")

    cursor.close()
    connection.close()


def run():
    st.title("Store Operations")

    # Customer Order History Section
    st.subheader("Customer Order History")
    customer_id = st.number_input("Customer ID")
    if st.button("Fetch Order History"):
        orders = customer_order_history(customer_id)
        if orders:
            st.write("Order History:")
            for order in orders:
                st.write(f"Order ID: {order[0]}")
                st.write(f"Date: {order[2]}")
                st.write(f"Total Price: {order[3]}")
                st.write(f"Status: {order[4]}")
                st.write("------")
        else:
            st.warning("No orders found for this customer")
    
    st.subheader("Average Price by Category")
    category_name = st.text_input("Enter Category Name:")
    if category_name:
        category_average_price = calculate_average_price_by_category(category_name)
        if category_average_price is not None:
            st.write(f"Average Price for {category_name}: ${category_average_price:.2f}")
        else:
            st.write(f"No data available for category: {category_name}")
    

    st.subheader("Total Transactions by Employee")
    employee_id = st.number_input("Enter Employee ID")

    if st.button("Get Transactions"):
        if employee_id:
            get_total_transactions_by_employee(employee_id)
        else:
            st.warning("Please enter an Employee ID")
        
    st.subheader('Low Stock Notifier')

    product_id = st.number_input('Enter Product ID')
    threshold_quantity = st.number_input('Enter Threshold Quantity')

    if st.button('Check Stock'):
        notification = get_low_stock_notifications(product_id, threshold_quantity)
        if notification:
            st.success(notification)
    
    st.subheader("Employee Lookup by Date of Birth")

    date_of_birth = st.date_input("Select Date of Birth")

    if st.button("Get Employees"):
        get_employees_by_dob(date_of_birth)
        

if __name__ == "__main__":
    run()

