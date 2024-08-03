import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website
base_url = "https://mccoymart.com"

# URL of the AAC blocks page
aac_blocks_url = f"{base_url}/buy/aac-blocks/"

# Send a GET request to the AAC blocks page
response = requests.get(aac_blocks_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # List to hold the scraped data
    products = []
    
    # Find all product containers (adjust the class name as per the actual HTML)
    product_containers = soup.find_all('div', class_='item-content')
    
    for container in product_containers:
        # Extract product name
        name = container.find('h3', class_='item-title').text.strip()
        
        # Extract product price
        price = container.find('div', class_='item-price').text.strip()
        
        # Extract product URL
        product_url = base_url + container.find('a')['href']
        
        # Request the individual product page
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.text, 'html.parser')
        
        # Extract additional details from the product page
        brand = product_soup.find('td', text='Brand').find_next_sibling('td').text.strip()
        model_no = product_soup.find('td', text='Model No').find_next_sibling('td').text.strip()
        material = product_soup.find('td', text='Material').find_next_sibling('td').text.strip()
        coverage = product_soup.find('td', text='Coverage (30kg)').find_next_sibling('td').text.strip()
        thickness = product_soup.find('td', text='Thickness').find_next_sibling('td').text.strip()
        description = product_soup.find('div', class_='product-desc-content').text.strip()
        
        # Store the extracted data in a dictionary
        product_data = {
            'name': name,
            'price': price,
            'brand': brand,
            'model_no': model_no,
            'material': material,
            'coverage': coverage,
            'thickness': thickness,
            'description': description,
            'product_url': product_url
        }
        
        # Add the product data to the list
        products.append(product_data)
    
    # Save the data to a JSON file
    with open('aac_blocks_products.json', 'w') as f:
        json.dump(products, f, indent=4)
    
    print("Data has been successfully scraped and saved to aac_blocks_products.json")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
