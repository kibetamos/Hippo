import requests
from bs4 import BeautifulSoup

# URL of the site to scrape
url = "https://www.hippostores.com/k-/productlist?sort=relevance"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product information
    products = []
    for product in soup.find_all('div', class_='product-card'):
        name = product.find('div', class_='product-title').text.strip()
        price = product.find('div', class_='product-price').text.strip()
        products.append({'name': name, 'price': price})

    # Print the products
    for product in products:
        print(f"Name: {product['name']}, Price: {product['price']}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
