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

# Function to create an employee
def create_employee(user_id, first_name, last_name, dob, salary, address, phone_number, hire_date):
    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = "INSERT INTO Employee (UserID, FirstName, LastName, DateOfBirth, Salary, Address, PhoneNumber, HireDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (user_id, first_name, last_name, dob, salary, address, phone_number, hire_date))

    connection.commit()
    st.success(f"Employee '{first_name}' created successfully.")

    cursor.close()
    connection.close()

# Function to read all employees
def read_employees():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Employee"
    cursor.execute(query)
    employees = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()

    return employees, column_names

# Function to display employees in a table
def display_employees_table():
    employees, column_names = read_employees()
    if employees:
        df = pd.DataFrame(employees, columns=column_names)
        st.write(df)
    else:
        st.write("No employees found.")

# Function to delete an employee by ID
def delete_employee(employee_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Employee WHERE EmployeeID = %s"
    cursor.execute(delete_query, (employee_id,))
    connection.commit()
    st.warning(f"Employee with ID {employee_id} deleted.")

    cursor.close()
    connection.close()

def update_employee(employee_id, user_id, first_name, last_name, dob, salary, address, phone_number, hire_date):
    connection = connect_to_db()
    cursor = connection.cursor()

    update_query = "UPDATE Employee SET UserID = %s, FirstName = %s, LastName = %s, DateOfBirth = %s, Salary = %s, Address = %s, PhoneNumber = %s, HireDate = %s WHERE EmployeeID = %s"
    cursor.execute(update_query, (user_id, first_name, last_name, dob, salary, address, phone_number, hire_date, employee_id))
    connection.commit()
    st.success(f"Employee with ID {employee_id} updated successfully.")

    cursor.close()
    connection.close()

# Function to retrieve employees for update
def update_employees():
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM Employee"
    cursor.execute(query)
    employees = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return employees


 

def run():
    st.title("Employees")

    operation = st.sidebar.selectbox("Select operation", ["Create", "Delete","Update"], index=0)

    if operation == "Create":
        # Display existing employees in a table
        display_employees_table()

        # Create new employee form
        st.write("### Create New Employee")
        user_id = st.number_input("User ID")
        dob = st.date_input("Date of Birth")
        salary = st.number_input("Salary")
        address = st.text_input("Address")
        phone_number = st.text_input("Phone Number")
        hire_date = st.date_input("Hire Date")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        if st.button("Create Employee"):
            create_employee(user_id, dob, salary, address, phone_number, hire_date,first_name, last_name)
    
    elif operation == "Update":
        # Display existing employees in a table
        display_employees_table()

        # Update employee by ID
        st.write("### Update Employee")
        employees = update_employees()
        employee_options = {f"{employee[1]} (ID: {employee[0]})": employee[0] for employee in employees}
        selected_employee = st.selectbox("Select Employee to Update", list(employee_options.keys()))
        employee_id = employee_options[selected_employee]

        updated_user_id = st.number_input("Updated User ID")

        updated_dob = st.date_input("Updated Date of Birth")
        updated_salary = st.number_input("Updated Salary")
        updated_address = st.text_input("Updated Address")
        updated_phone_number = st.text_input("Updated Phone Number")
        updated_hire_date = st.date_input("Updated Hire Date")
        updated_first_name = st.text_input("Updated First Name")
        updated_last_name=st.text_input("Updated Last Name")
        if st.button("Update Employee"):
            update_employee(employee_id, updated_user_id, updated_dob, updated_salary, updated_address, updated_phone_number, updated_hire_date, updated_first_name, updated_last_name)
        else:
            st.write("No employees found for updating.")
    elif operation == "Delete":
        # Display existing employees in a table
        display_employees_table()

        # Delete employee by ID
        st.write("### Delete Employee")
        employee_id_to_delete = st.number_input("Enter Employee ID to delete", min_value=1)
        if st.button("Delete Employee"):
            delete_employee(employee_id_to_delete)

if __name__ == "__main__":
    run()

