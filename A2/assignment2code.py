import pandas as pd
import pyarrow
import ssl
import time
import sys

ssl._create_default_https_context = ssl._create_unverified_context
pd.set_option("display.max_rows", None)

# Execute the CSV file operation
def load_csv(file_path):
    try:
        print(f"Reading CSV file: {file_path}")
        start_time = time.time()
        sales_data = pd.read_csv(file_path, dtype_backend='pyarrow', on_bad_lines="skip").fillna(0) # ChatGPT was used to generate fillna.
        load_time = time.time() - start_time  
        print(f"File loaded in {load_time:.2f} seconds")
        print(f"Number of rows: {len(sales_data)}")
        print(f"Columns available: {sales_data.columns.to_list()}")
        
        # Verify the column specifications
        required_columns = ['quantity', 'order_date', 'unit_price', 'sales_region', 'employee_id', 'order_type']
        missing_columns = [col for col in required_columns if col not in sales_data.columns]
        if missing_columns:
            print(f"Warning: Missing columns - {missing_columns}. Some analytics may not work.")
        
        sales_data['order_date'] = pd.to_datetime(sales_data['order_date'], errors='coerce')

        # Sales data summary
        summarize_data(sales_data)

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

# Sales data summarization procedure
def summarize_data(data):
    total_orders = len(data)
    total_employees = data['employee_id'].nunique()
    sales_regions = data['sales_region'].nunique()
    date_range = (data['order_date'].min(), data['order_date'].max())
    unique_customers = data['customer_id'].nunique() if 'customer_id' in data.columns else 0
    product_categories = data['product_category'].nunique() if 'product_category' in data.columns else 0
    unique_states = data['customer_state'].nunique() if 'customer_state' in data.columns else 0
    total_sales_amount = data['unit_price'].sum()
    total_quantities = data['quantity'].sum()

    print("\n--- Sales Data Summary ---")
    print(f"Total Orders: {total_orders}")
    print(f"Number of Employees: {total_employees}")
    print(f"Sales Regions: {sales_regions}")
    print(f"Date Range of Orders: {date_range[0]} to {date_range[1]}")
    print(f"Number of Unique Customers: {unique_customers}")
    print(f"Product Categories: {product_categories}")
    print(f"Unique States: {unique_states}")
    print(f"Total Sales Amount: {total_sales_amount:.2f}")
    print(f"Total Quantities Sold: {total_quantities}")

# An option to export a DataFrame as an Excel file
def export_to_excel(df, filename):
    try:
        df.to_excel(filename, index=False)
        print(f"Results exported to {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while exporting to Excel: {e}")

# Displays the first n rows of data
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
    if export_results(result): # The export procedures were developed utilizing ChatGPT by way of the prompt.
        filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
        export_to_excel(result, filename)

def average_sales_by_region_and_average_sales_by_state_and_sale_type(data):
    result = pd.pivot_table(data, values='unit_price', index=['sales_region', 'customer_state'], columns='order_type', aggfunc='mean')
    print("\nAverage Sales by Region, State, and Sale Type")
    print(result)
    if export_results(result):
        filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
        export_to_excel(result, filename)

def sales_by_customer_type_and_order_type_by_state(data):
    if 'customer_state' not in data.columns:
        print("Error: 'customer_state' column is missing from the data. Cannot generate this report.")
        return
    
    result = pd.pivot_table(data, values='quantity', index=['customer_state', 'customer_type'], columns='order_type', aggfunc='sum')
    print("\nSales by Customer Type and Order Type by State")
    print(result)
    if export_results(result):
        filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
        export_to_excel(result, filename)

def total_sales_quantity_and_price_by_region_and_product(data):
    result = pd.pivot_table(data, values=['quantity', 'unit_price'], index=['sales_region', 'product_category'], aggfunc='sum')
    print("\nTotal Sales Quantity and Price by Region and Product")
    print(result)
    if export_results(result):
        filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
        export_to_excel(result, filename)

def total_sales_quantity_and_price_by_customer_type(data):
    result = pd.pivot_table(data, values=['quantity', 'unit_price'], index=['order_type', 'customer_type'], aggfunc='sum')
    print("\nTotal Sales Quantity and Price by Customer Type")
    print(result)
    if export_results(result):
        filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
        export_to_excel(result, filename)

def max_min_sales_price_by_category(data):
    result = pd.pivot_table(data, values='unit_price', index='product_category', aggfunc=['max', 'min'])
    print("\nMax and Min Sales Price by Category")
    print(result)
    if export_results(result):
        filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
        export_to_excel(result, filename)

def employees_by_region(data):
    result = pd.pivot_table(data, index="sales_region", values="employee_id", aggfunc=pd.Series.nunique)
    print("\nNumber of Unique Employees by Region")
    result.columns = ['Number of Employees']
    print(result)
    if export_results(result):
        filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
        export_to_excel(result, filename)

# Customizes pivot tables to user needs
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
        "2": "unit_price"
    }
    
    print("\nSelect values (choose number(s), separated by commas):")
    for key, value in value_options.items():
        print(f"{key}. {value}")
    value_choice = input("Your choice: ").strip().split(',')
    selected_values = [value_options.get(choice.strip()) for choice in value_choice if choice.strip() in value_options]
    
    # Aggregation functions selection
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
    
    # Build the pivot table according to the selected options
    if selected_rows and selected_values and selected_aggfunc:
        try:
            result = pd.pivot_table(data, values=selected_values, index=selected_rows, columns=selected_columns, aggfunc=selected_aggfunc)
            print("\nCustom Pivot Table")
            print(result)
            if export_results(result):
                filename = input("Enter the filename for the Excel export (e.g., results.xlsx): ")
                export_to_excel(result, filename)
        except Exception as e:
            print(f"An error occurred creating the pivot table: {e}")
    else:
        print("No valid selections made for creating the pivot table.")

# The option to terminate the application
def exit_program(data):
    print("Exiting the program.")
    sys.exit(0)

# Supports for exporting output
def export_results(result):
    choice = input("Would you like to export the results to an Excel file? (yes/no): ").strip().lower()
    return choice == 'yes'

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

    # Remove menu options that are not applicable based on missing columns
    # ChatGPT was heavily relied upon in response to a specific prompt concerning missing columns.
    if 'customer_state' not in data.columns:
        menu_options.remove(menu_options[2])  # Sales by customer type and order type by state

    if 'product_category' not in data.columns:
        menu_options.remove(menu_options[3])  # Total sales quantity and price by region and product

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

# Call load_csv to load the file
url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
sales_data = load_csv(url)

# Main loop for user interaction
def main():
    while True:
        display_menu(sales_data)

# If this is the main program, call main()
if __name__ == "__main__":
    main()