import requests
from bs4 import BeautifulSoup

url = 'https://materialdepot.in/acrylic-laminates-for-kitchen?handle=acrylic-laminates-for-kitchen&page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all product containers
products = soup.find_all('div', class_='product_list_product_card_container___Y3Ko')

# Count the total number of products on the current page
total_products = len(products)

print(f"Total number of products on this page: {total_products}")
