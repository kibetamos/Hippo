import requests
from bs4 import BeautifulSoup

# Function to extract the number of products from a page
def count_products_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product containers
    products = soup.find_all('div', class_='product_list_product_card_container___Y3Ko')
    
    # Return the count of products on this page
    return len(products)

# Base URL for the pages
base_url = 'https://materialdepot.in/acrylic-laminates-for-kitchen?handle=acrylic-laminates-for-kitchen&page={}'

# Iterate through the first 5 pages and count products
total_products = 0
for page in range(1, 6):  # Pages 1 to 5
    url = base_url.format(page)
    page_products = count_products_on_page(url)
    print(f"Total number of products on page {page}: {page_products}")
    total_products += page_products

print(f"Total number of products across 5 pages: {total_products}")
