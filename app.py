import streamlit as st
import importlib


def main():
    st.title('Grocery Store Management')

    pages = {
        'Role': 'role_page',
        'User': 'user_page',
        'Employee': 'employee_page',
        'Supplier': 'supplier_page',
        'Customer': 'customer_page',
        'Store': 'store_page',
        'Category': 'category_page',
        'Product': 'product_page',
        'OrderTable': 'order_page',
        'Transaction': 'transaction_page',
        'OrderDetails': 'order_details_page',
        'Store Analytics':'store_op',
        'Store Operations':'store_op1'
    }

    selected_page = st.sidebar.selectbox('Select Table', list(pages.keys()))

    module_name = pages[selected_page]
    module = importlib.import_module(module_name)
    module.run()

if __name__ == "__main__":
    main()