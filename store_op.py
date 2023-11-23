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
        print(f"Error connecting to MySQL database: {e}")
        return None

# Function to calculate average price of products
def calculate_average_product_price():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT AVG(Price) FROM Product"
    cursor.execute(query)
    average_price = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return average_price

# Function to calculate total transaction amount
def calculate_total_transactions_amount():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT SUM(TransactionAmount) FROM Transaction"
    cursor.execute(query)
    total_amount = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_amount

# Function to fetch top selling products
def top_selling_products(n=5):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = """
    SELECT p.Name, SUM(od.QuantityOrdered) as TotalQuantitySold
    FROM Product p
    JOIN OrderDetails od ON p.ProductID = od.ProductID
    GROUP BY p.ProductID
    ORDER BY TotalQuantitySold DESC
    LIMIT %s
    """
    cursor.execute(query, (n,))
    top_products = cursor.fetchall()

    cursor.close()
    connection.close()

    return top_products

# Function to find employees by store
def find_employees_by_store(store_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = """
    SELECT e.Name
    FROM Employee e
    JOIN Store s ON e.EmployeeID = s.Manager
    WHERE s.StoreID = %s
    """
    cursor.execute(query, (store_id,))
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return employees

def fetch_employee_details(employee_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = f"SELECT * FROM Employee WHERE EmployeeID = {employee_id}"
    cursor.execute(query)
    employee_details = cursor.fetchall()

    cursor.close()
    connection.close()

    return employee_details

def fetch_product_details(product_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = f"SELECT * FROM Product WHERE ProductID = {product_id}"
    cursor.execute(query)
    product_details = cursor.fetchall()

    cursor.close()
    connection.close()

    return product_details

def fetch_store_details(store_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = f"SELECT * FROM Store WHERE StoreID = {store_id}"
    cursor.execute(query)
    store_details = cursor.fetchall()

    cursor.close()
    connection.close()

    return store_details


# Function to call CalculateExperienceLength function in MySQL
def calculate_experience_length(employee_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute(f"SELECT CalculateExperienceLength({employee_id})")
        experience_length = cursor.fetchone()[0]

        st.write(f"Experience for Employee ID {employee_id}: {experience_length} years")

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        st.error(f"Error calculating experience length: {e}")

# Function to fetch orders by status
def get_orders_by_status(order_status):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        query='CALL GetOrdersByStatus(%s)'
        cursor.execute(query, (order_status,))
        orders = cursor.fetchall()

        for order in orders:
            st.table(order)  # Display order information

    except mysql.connector.Error as e:
        st.error(f"Error fetching orders by status: {e}")

    cursor.close()
    connection.close()

def run():
    st.title("Store Analytics")

    average_price = calculate_average_product_price()
    total_amount = calculate_total_transactions_amount()

    st.write(f"Average Price of Products: ${average_price:.2f}")
    st.write(f"Total Transaction Amount: ${total_amount:.2f}")

    st.subheader("Top Selling Products")
    top_products = top_selling_products()
    for product in top_products:
        st.write(f"{product[0]} - Total Quantity Sold: {product[1]}")

    
    st.subheader('Calculate Employee Experience Length')

    employee_id = st.number_input('Enter Employee ID:', min_value=1, step=1)
    if st.button('Calculate'):
        experience_length = calculate_experience_length(employee_id)

    st.subheader('Fetch Employee Details')
    employee_id_input = st.number_input('Enter Employee ID:', min_value=1, step=1,key='employee_id_input')
    if st.button('Fetch Employee Details'):
        employee_details = fetch_employee_details(employee_id_input)
        if employee_details:
            st.write("Employee Details:")
            for detail in employee_details:
                st.table(detail)
        else:
            st.write("No employee found with that ID.")

    st.subheader('Fetch Product Details')
    product_id_input = st.number_input('Enter Product ID:', min_value=1, step=1,key='product_id_input')
    if st.button('Fetch Product Details'):
        product_details = fetch_product_details(product_id_input)
        if product_details:
            st.write("Product Details:")
            for detail in product_details:
                st.table(detail)
        else:
            st.write("No product found with that ID.")

    st.subheader('Fetch Store Details')
    store_id_input = st.number_input('Enter Store ID:', min_value=1, step=1,key='store_id_input')
    if st.button('Fetch Store Details'):
        store_details = fetch_store_details(store_id_input)
        if store_details:
            st.write("Store Details:")
            for detail in store_details:
                st.table(detail)
        else:
            st.write("No store found with that ID.")
    
    st.subheader("Order Status Lookup")

    order_status = st.text_input('Enter Order Status (e.g.,shipped):')
    if st.button('Fetch Orders'):
        get_orders_by_status(order_status)
        


    
    
    
    

if __name__ == "__main__":
    run()
