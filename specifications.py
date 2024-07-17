from bs4 import BeautifulSoup
import requests

url = "https://www.hippostores.com/havells-63a-100ma-fp-rccb-tog-type-ac-stad-x-model-dhrzcmff100063/product/1000002303"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting product name
product_name_elem = soup.find('h4', class_='c126 c110 c134')
if product_name_elem:
    product_name = product_name_elem.text.strip()
    print(f"Product Name: {product_name}")
else:
    print("Product name not found or may be loaded dynamically")
