import pandas as pd
import os

def xlsx_to_csv(xlsx_file, output_folder=None):
    # Load the Excel file
    try:
        excel_data = pd.read_excel(xlsx_file, sheet_name=None)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return

    # Determine the output folder
    if output_folder is None:
        output_folder = os.path.dirname(xlsx_file)

    # Convert each sheet to a CSV file
    for sheet_name, data in excel_data.items():
        csv_file_name = f"{sheet_name}.csv"
        csv_file_path = os.path.join(output_folder, csv_file_name)
        
        try:
            data.to_csv(csv_file_path, index=False, encoding='utf-8')
            print(f"Successfully converted '{sheet_name}' to '{csv_file_path}'")
        except Exception as e:
            print(f"Error saving the CSV file: {e}")

if __name__ == "__main__":
    xlsx_file = "Deep/Hippo_scraper_from_243.xlsx"  # Replace with your Excel file path
    output_folder = "Deep/"  # Replace with your desired output directory or set to None
    xlsx_to_csv(xlsx_file, output_folder)
