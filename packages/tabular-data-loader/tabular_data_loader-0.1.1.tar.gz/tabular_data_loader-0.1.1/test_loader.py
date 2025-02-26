import io
import os
from tabular_data_loader import load_tabular_data
from datetime import datetime

def print_row(data, types):
    print("  Data:", ", ".join(map(str, data)))
    print("  Types:", ", ".join(types))

def print_data_with_types(data, types):
    for i, (row_data, row_types) in enumerate(zip(data, types)):
        print(f"Row {i}:")
        print_row(row_data, row_types)
        print()

def test_csv():
    csv_content = b"""col1,col2,col3,col4
100,3.14,text,2024-02-25
200,6.28,sample,2024-02-25 14:30:00"""
    data, types = load_tabular_data(csv_content)
    print("CSV Test:")
    print_data_with_types(data, types)
    print()

def test_excel():
    # Create a simple Excel file with multiple sheets
    from openpyxl import Workbook
    wb = Workbook()
    
    # First sheet (default)
    ws1 = wb.active
    ws1.title = "Employees"
    ws1.append(['Name', 'Age', 'Start Date', 'Last Login'])
    ws1.append(['John', 30, '2024-01-01', '2024-02-25 09:30:00'])
    ws1.append(['Alice', 25, '2024-02-01', '2024-02-25 10:15:00'])
    
    # Second sheet
    ws2 = wb.create_sheet("Departments")
    ws2.append(['Department', 'Budget', 'Created At'])
    ws2.append(['Engineering', 1000000.50, '2024-01-01 00:00:00'])
    ws2.append(['Marketing', 500000.75, '2024-02-01 00:00:00'])
    
    # Save to a temporary file first
    temp_file = "temp_test.xlsx"
    wb.save(temp_file)
    
    # Read the file content
    with open(temp_file, "rb") as f:
        excel_content = f.read()
    
    # Clean up
    os.remove(temp_file)
    
    data, types = load_tabular_data(excel_content)
    print("Excel Test (Multiple Sheets):")
    print_data_with_types(data, types)

if __name__ == "__main__":
    test_csv()
    test_excel()
