import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the site to scrape
base_url = "https://www.hippostores.com/k-/productlist?sort=relevance"

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to fetch product description and specifications
def fetch_product_description_and_sku(link):
    try:
        product_response = requests.get(link, headers=headers)
        product_response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        # Find all specification keys and values
        spec_keys = product_soup.find_all('div', class_='pdp_specsKey__5LWXC')
        spec_values = product_soup.find_all('div', class_='pdp_specsValue__fDPie')

        # Create a dictionary to store specifications
        specifications = {}
        for key, value in zip(spec_keys, spec_values):
            key_text = key.find('p').text.strip()
            value_text = value.find('p').text.strip()
            specifications[key_text] = value_text

        # Extract SKU code from the URL
        sku_code = link.split('/')[-1]

        return sku_code, specifications
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product from {link}: {e}")
        return "SKU fetch error", {}

# Send a GET request to the website
response = requests.get(base_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product information
    products = []

    # Check the structure of the product card divs
    product_cards = soup.find_all('div', class_='productCardRevamped_container__aJ6lA')

    if not product_cards:
        print("No product cards found. Please check the class name or HTML structure.")
    else:
        for product in product_cards:
            # Adjust the class names based on the actual HTML structure
            name_tag = product.find('div', class_='productCardRevamped_productName__aEF8u')
            price_tag = product.find('div', class_='productCardRevamped_price__cWkdn')
            mrp_tag = product.find('span', class_='productCardRevamped_mrpPrice__Yz_Yd')
            discount_tag = product.find('div', class_='productCardRevamped_discount__GSjgY')
            link_tag = product.find_parent('a', href=True)  # Assuming the link is in a parent 'a' tag
            brand_tag = product.find('div', class_='productCardRevamped_brandContainer__1mgym')  # Brand tag

            if name_tag and price_tag and link_tag and brand_tag:
                name = name_tag.text.strip()
                price = price_tag.text.strip()
                mrp = mrp_tag.text.strip() if mrp_tag else "N/A"
                discount = discount_tag.text.strip() if discount_tag else "N/A"
                brand = brand_tag.text.strip()  # Extract brand
                link = link_tag['href']

                # Check if the link has a scheme, if not prepend the base URL
                if not link.startswith('https://'):
                    full_link = urljoin(base_url, link)
                else:
                    full_link = link

                # Fetch the SKU code and specifications
                sku_code, specifications = fetch_product_description_and_sku(full_link)

                products.append({
                    'name': name,
                    'price': price,
                    'mrp': mrp,
                    'discount': discount,
                    'brand': brand,  # Add brand to the product details
                    'link': full_link,
                    'sku_code': sku_code,
                    'specifications': specifications
                })
            else:
                print("Product title, price tag, link, or brand not found. Please check the class names.")

        # Print the products
        for product in products:
            print(f"Name: {product['name']}")
            print(f"Price: {product['price']}, MRP: {product['mrp']}, Discount: {product['discount']}")
            print(f"Brand: {product['brand']}")
            print(f"SKU Code: {product['sku_code']}")
            print("Specifications:")
            for key, value in product['specifications'].items():
                print(f"{key}: {value}")
            print(f"Link: {product['link']}")
            print("-----------------------------")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
