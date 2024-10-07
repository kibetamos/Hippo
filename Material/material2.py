import requests
from bs4 import BeautifulSoup
import pandas as pd
import re  # For regular expression

# Function to extract product specifications from a product page
def scrape_product_specifications(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find specifications section
    specifications = []
    
    spec_div = soup.find('div', class_='th-fontSize-16 th-fontWeight-600 pb-4')
    if spec_div:
        specs = spec_div.find_next_siblings('div', class_='py-1')
        for spec in specs:
            label = spec.find('div', class_='col-4 th-fontSize-14 th-fontWeight-500 grey-color2-text').text.strip()
            value = spec.find('div', class_='col-8 d-flex justify-content-start').text.strip()
            specifications.append(f"{label}: {value}")

    return specifications

# Function to extract breadcrumb path from a product page
def scrape_breadcrumb(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    breadcrumb = []
    breadcrumb_div = soup.find('nav', {'aria-label': 'breadcrumb'})
    if breadcrumb_div:
        breadcrumb_items = breadcrumb_div.find_all('li', class_='breadcrumb-item')
        # Collect all items except the first (Home) and last (product name)
        for item in breadcrumb_items[1:-1]:  # Exclude the first (Home) and last (product name) items
            link_text = item.get_text(strip=True)
            breadcrumb.append(link_text)
    return breadcrumb  # Return breadcrumb as a list of categories

# Function to extract product details from a page
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product containers
    products = soup.find_all('div', class_='product_list_product_card_container___Y3Ko')
    
    product_data = []
    for product in products:
        try:
            # Extract product URL
            product_url = product.find('a', class_='product_card_product_card_container__6KFv9')['href']
            product_url = f"https://materialdepot.in{product_url}"

            # Extract product category
            product_category = product.find('div', class_='th-fontWeight-500 th-fontWeight-md-700 grey-color1-text th-fontSize-14 text-uppercase mt-1 product_card_text_ellipsis_one_line__qhntH')
            product_category = product_category.text.strip() if product_category else "N/A"
            
            # Extract product name
            product_name = product.find('div', class_='th-fontSize-12 py-1 th-fontWeight-400 th-md-fontWeight-400 grey-color1-text product_card_text_ellipsis_two_line__RU0__')
            product_name = product_name.text.strip() if product_name else "N/A"
            
            # Extract price per Sq. Ft.
            price_per_sq_ft = product.find('div', class_='col-md-6 col-6 d-flex align-items-start flex-column')
            price_per_sq_ft = price_per_sq_ft.text.strip().replace('₹', '').replace('/Sq. Ft.', '').strip() if price_per_sq_ft else "N/A"
            
            # Extract price per sheet
            price_per_sheet = product.find('div', class_='align-items-md-end align-items-end col-md-6 col-6 d-flex flex-column')
            price_per_sheet = price_per_sheet.text.strip().replace('₹', '').replace('/Sheet', '').strip() if price_per_sheet else "N/A"
            
            # Extract MRP and discount
            mrp_discount = product.find('div', class_='d-flex justify-content-between')
            if mrp_discount:
                mrp = mrp_discount.find('span', class_='text-decoration-line-through')
                mrp = mrp.text.strip().replace('₹', '').strip() if mrp else "N/A"
                
                discount = mrp_discount.find('span', class_='green-color-text')
                discount = discount.text.strip() if discount else "N/A"
                
                # Use regex to extract only the number and percentage
                discount_match = re.search(r'(\d+)%?', discount)
                discount = discount_match.group(0) if discount_match else "N/A"  # Keep only the number and '%' if present
            else:
                mrp = "N/A"
                discount = "N/A"

            # Extract product specifications
            specifications = scrape_product_specifications(product_url)
            specifications_str = '; '.join(specifications)  # Join specifications into a single string

            # Extract breadcrumb path without "Home" and the product name
            breadcrumb = scrape_breadcrumb(product_url)
            path = ' > '.join(breadcrumb)  # Join breadcrumb items into a single string
            
            # Store data
            product_entry = {
                'Product URL': product_url,
                'Product Name': product_name,
                'Category': product_category,
                'MRP': mrp,
                'Discount': discount,
                'Price per Sq. Ft.': price_per_sq_ft,
                'Price per Sheet': price_per_sheet,
                'Specifications': specifications_str,  # Store specifications as a single string
                'Path': path,  # Store breadcrumb path as a single string
            }

            # Add category columns dynamically
            for i, category in enumerate(breadcrumb):
                product_entry[f'Category {i + 1}'] = category

            product_data.append(product_entry)
        except Exception as e:
            print(f"Error extracting product: {e}")
    
    return product_data

# Base URL for the pages
base_url = 'https://materialdepot.in/acrylic-laminates-for-kitchen?handle=acrylic-laminates-for-kitchen&page={}'

# Initialize an empty list to collect all product data
all_products = []

# Iterate through pages 1 to 5 (or more if needed)
for page in range(1, 2):  # Adjust range as needed
    url = base_url.format(page)
    print(f"Scraping page {page}...")
    products = scrape_product_details(url)
    all_products.extend(products)

# Create a DataFrame using pandas
df = pd.DataFrame(all_products)

# Save the DataFrame to an Excel file
excel_filename = 'products.xlsx'
df.to_excel(excel_filename, index=False)

print(f"Data saved to '{excel_filename}'.")
