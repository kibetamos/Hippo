import pandas as pd

# Load the Excel file
input_file = 'Data1.xlsx'
df = pd.read_excel(input_file)

# Define a function to clean a row based on the provided structure
def clean_row(row):
    # Create a dictionary with the provided data structure
    cleaned_data = {
        'Brand': row.get('Brand', '').strip(),
        'Color': row.get('Color', '').strip(),
        'Compressive Strength': row.get('Compressive Strength', '').strip(),
        'Dry Density': row.get('Dry Density', '').strip(),
        'Model No': row.get('Model No', '').strip(),
        'Shape': row.get('Shape', '').strip(),
        'Size': row.get('Size', '').strip(),
        'Sound Absorption': row.get('Sound Absorption', '').strip(),
        'Thermal Conductivity Range (k Value)': row.get('Thermal Conductivity Range (k Value)', '').strip(),
        'Water absorption': row.get('Water absorption', '').strip()
    }
    return pd.Series(cleaned_data)

# Apply the cleaning function to each row
df_cleaned = df.apply(clean_row, axis=1)

# Save the cleaned DataFrame to a new Excel file
output_file = 'cleaned_file.xlsx'
df_cleaned.to_excel(output_file, index=False)

print(f"Cleaned file saved as {output_file}")
