import pandas as pd
import pyarrow
import ssl
import time
import sys

ssl._create_default_https_context = ssl._create_unverified_context
pd.set_option("display.max_rows", None)

# Load the CSV file function
def load_csv(file_path):
    try:
        print(f"Reading CSV file: {file_path}")
        start_time = time.time()
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip").fillna(0)
        load_time = time.time() - start_time  
        print(f"File loaded in {load_time:.2f} seconds")
        print(f"Number of rows: {len(sales_data)}")
        print(f"Columns available: {sales_data.columns.to_list()}")
        
        # Check for required columns
        required_columns = ['quantity', 'order_date', 'unit_price', 'sales_region', 'employee_id', 'order_type']
        missing_columns = [col for col in required_columns if col not in sales_data.columns]
        if missing_columns:
            print(f"Warning: Missing columns - {missing_columns}. Some analytics may not work.")
        
        sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], format="mixed")
        return sales_data

    except FileNotFoundError:
        print("Error: The specified file was not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")
        sys.exit(1)

# Function to display the first n rows of data
def display_rows(data):
    numRows = len(data)
    print("\nEnter number of rows to display:")
    print(f"- Enter a number between 1 and {numRows}")
    print("- To see all rows enter 'all'")
    print("- To skip, press Enter")
    user_choice = input("Your choice: ").strip().lower()

    if user_choice == '':
        print("Skipping preview")
    elif user_choice == 'all':
        print(data)
    elif user_choice.isdigit() and 1 <= int(user_choice) <= numRows:
        print(data.head(int(user_choice)))
    else:
        print("Invalid input. Please enter a valid number or 'all'.")

# Analytical tasks
def total_sales_by_region_and_order_type(data):
    result = pd.pivot_table(data, values='quantity', index='sales_region', columns='order_type', aggfunc='sum')
    print("\nTotal Sales by Region and Order Type")
    print(result)

def average_sales_by_region_and_average_sales_by_state_and_sale_type(data):
    result = pd.pivot_table(data, values='unit_price', index=['sales_region', 'customer_state'], columns='order_type', aggfunc='mean')
    print("\nAverage Sales by Region, State, and Sale Type")
    print(result)

def sales_by_customer_type_and_order_type_by_state(data):
    if 'customer_state' not in data.columns:
        print("Error: 'customer_state' column is missing from the data. Cannot generate this report.")
        return
    
    result = pd.pivot_table(data, values='quantity', index=['customer_state', 'customer_type'], columns='order_type', aggfunc='sum')
    print("\nSales by Customer Type and Order Type by State")
    print(result)

def total_sales_quantity_and_price_by_region_and_product(data):
    result = pd.pivot_table(data, values=['quantity', 'unit_price'], index=['sales_region', 'produce_name'], aggfunc='sum')
    print("\nTotal Sales Quantity and Price by Region and Product")
    print(result)

def total_sales_quantity_and_price_by_customer_type(data):
    result = pd.pivot_table(data, values=['quantity', 'unit_price'], index=['order_type', 'customer_type'], aggfunc='sum')
    print("\nTotal Sales Quantity and Price by Customer Type")
    print(result)

def max_min_sales_price_by_category(data):
    result = pd.pivot_table(data, values='unit_price', index='product_category', aggfunc=['max', 'min'])
    print("\nMax and Min Sales Price by Category")
    print(result)

def employees_by_region(data):
    result = pd.pivot_table(data, index="sales_region", values="employee_id", aggfunc=pd.Series.nunique)
    print("\nNumber of Unique Employees by Region")
    result.columns = ['Number of Employees']
    print(result)

# Custom pivot table functionality
def custom_pivot_table(data):
    print("\n--- Custom Pivot Table Generator ---")
    
    # Rows selection
    row_options = {
        "1": "employee_name",
        "2": "sales_region",
        "3": "product_category"
    }
    
    print("Select rows (choose number(s), separated by commas):")
    for key, value in row_options.items():
        print(f"{key}. {value}")
    row_choice = input("Your choice: ").strip().split(',')
    selected_rows = [row_options.get(choice.strip()) for choice in row_choice if choice.strip() in row_options]
    
    # Columns selection
    column_options = {
        "1": "order_type",
        "2": "customer_type"
    }
    
    print("\nSelect columns (optional, choose number(s), separated by commas, or press Enter for no grouping):")
    for key, value in column_options.items():
        print(f"{key}. {value}")
    column_choice = input("Your choice: ").strip().split(',')
    selected_columns = [column_options.get(choice.strip()) for choice in column_choice if choice.strip() in column_options]
    
    # Values selection
    value_options = {
        "1": "quantity",
        "2": "sale_price"
    }
    
    print("\nSelect values (choose number(s), separated by commas):")
    for key, value in value_options.items():
        print(f"{key}. {value}")
    value_choice = input("Your choice: ").strip().split(',')
    selected_values = [value_options.get(choice.strip()) for choice in value_choice if choice.strip() in value_options]
    
    # Aggregation function selection
    agg_options = {
        "1": "sum",
        "2": "mean",
        "3": "count"
    }
    
    print("\nSelect aggregation function (choose number(s), separated by commas):")
    for key, value in agg_options.items():
        print(f"{key}. {value}")
    agg_choice = input("Your choice: ").strip().split(',')
    selected_aggfunc = [agg_options.get(choice.strip()) for choice in agg_choice if choice.strip() in agg_options]
    
    # Create the pivot table if selections were made
    if selected_rows and selected_values and selected_aggfunc:
        try:
            result = pd.pivot_table(data, values=selected_values, index=selected_rows, columns=selected_columns, aggfunc=selected_aggfunc)
            print("\nCustom Pivot Table")
            print(result)
        except Exception as e:
            print(f"An error occurred creating the pivot table: {e}")
    else:
        print("No valid selections made for creating the pivot table.")

# Exit program function
def exit_program(data):
    print("Exiting the program.")
    sys.exit(0)

# Display the top-level menu
def display_menu(data):
    menu_options = [
        ("Show the first n rows of sales data", display_rows),
        ("Total sales by region and order_type", total_sales_by_region_and_order_type),
        ("Average sales by region with average sales by state and sale type", average_sales_by_region_and_average_sales_by_state_and_sale_type),
        ("Sales by customer type and order type by state", sales_by_customer_type_and_order_type_by_state),
        ("Total sales quantity and price by region and product", total_sales_quantity_and_price_by_region_and_product),
        ("Total sales quantity and price by customer type", total_sales_quantity_and_price_by_customer_type),
        ("Max and min sales price of sales by category", max_min_sales_price_by_category),
        ("Number of unique employees by region", employees_by_region),
        ("Create a custom pivot table", custom_pivot_table),
        ("Exit", exit_program)
    ]

    print("\n--- Sales Data Dashboard ---")
    for index, (description, _) in enumerate(menu_options):
        print(f"{index + 1}. {description}")

    try:
        choice = int(input(f"Select an option (1-{len(menu_options)}): "))
        if 1 <= choice <= len(menu_options):
            menu_options[choice - 1][1](data)
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Please enter a valid number.")

# Load the sales data file
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
sales_data = load_csv(url)

# Main loop for user interaction
def main():
    while True:
        display_menu(sales_data)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()