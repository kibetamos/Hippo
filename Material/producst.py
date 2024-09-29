import requests
from bs4 import BeautifulSoup

# Function to extract product information
def extract_product_info(product):
    # Extract product name
    name = product.find('div', class_='product_card_text_ellipsis_two_line__RU0__')['data-bs-title']
    
    # Extract price per square foot
    price_sq_ft = product.find('div', text='₹').text.strip() if product.find('div', text='₹') else 'N/A'
    
    # Extract price per sheet
    price_per_sheet = product.find_all('div', class_='th-fontSize-14 th-md-fontSize-16 th-fontWeight-700 py-2 row')[0].find_all('div')[1].text.strip()
    
    # Extract the image URL
    img_url = product.find('img', class_='product_card_product_card_main_img__TYLKl')['src']
    
    # Extract MRP and discount
    mrp_info = product.find('div', class_='th-fontSize-12 th-fontWeight-500 grey-color-text')
    mrp = mrp_info.find('span', class_='text-decoration-line-through').text if mrp_info else 'N/A'
    discount = mrp_info.find('span', class_='green-color-text').text if mrp_info else 'N/A'
    
    # Extract additional attributes like thickness and finish
    badges = product.find_all('div', class_='product_card_card_badge__FjnMA')
    thickness = badges[0].text.strip() if len(badges) > 0 else 'N/A'
    finish = badges[1].text.strip() if len(badges) > 1 else 'N/A'
    
    # Return product details as a dictionary
    return {
        'name': name,
        'price_per_sq_ft': price_sq_ft,
        'price_per_sheet': price_per_sheet,
        'image_url': img_url,
        'mrp': mrp,
        'discount': discount,
        'thickness': thickness,
        'finish': finish
    }

# Function to extract the number of products from a page and their details
def count_products_and_extract_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product containers
    products = soup.find_all('div', class_='product_list_product_card_container___Y3Ko')
    
    # Extract details of all products on this page
    product_details = [extract_product_info(product) for product in products]
    
    # Return the count of products and the details
    return len(products), product_details

# Base URL for the pages
base_url = 'https://materialdepot.in/acrylic-laminates-for-kitchen?handle=acrylic-laminates-for-kitchen&page={}'

# Iterate through the first 5 pages and count products
total_products = 0
all_product_details = []
for page in range(1, 3):  # Pages 1 to 5
    url = base_url.format(page)
    page_products, product_details = count_products_and_extract_details(url)
    
    print(f"Total number of products on page {page}: {page_products}")
    total_products += page_products
    all_product_details.extend(product_details)

# Print the total number of products
print(f"Total number of products across 5 pages: {total_products}")

# Print the details of all products
for i, product in enumerate(all_product_details, 1):
    print(f"\nProduct {i}:")
    for key, value in product.items():
        print(f"{key}: {value}")
