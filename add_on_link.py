import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the site to scrape
base_url = "https://www.hippostores.com/k-/productlist?sort=relevance"

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to fetch product name and specifications from product detail page
def fetch_product_details(link):
    try:
        product_response = requests.get(link, headers=headers)
        product_response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        # Find the product name element
        name_tag = product.find('div', class_='productCardRevamped_productName__aEF8u')

        if name_tag:
            product_name = name_tag.text.strip()
        else:
            product_name = "Product name not found"

        # Find all specification keys and values
        spec_keys = product_soup.find_all('div', class_='pdp_specsKey__5LWXC')
        spec_values = product_soup.find_all('div', class_='pdp_specsValue__fDPie')

        # Create a dictionary to store specifications
        specifications = {}
        for key, value in zip(spec_keys, spec_values):
            key_text = key.find('p').text.strip()
            value_text = value.find('p').text.strip()
            specifications[key_text] = value_text

        return product_name, link, specifications
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product from {link}: {e}")
        return "Error fetching product details", link, {}

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
            link_tag = product.find_parent('a', href=True)  # Assuming the link is in a parent 'a' tag

            if link_tag:
                link = link_tag['href']

                # Check if the link has a scheme, if not prepend the base URL
                if not link.startswith('https://'):
                    full_link = urljoin(base_url, link)
                else:
                    full_link = link

                # Fetch the product details
                product_name, product_link, specifications = fetch_product_details(full_link)

                products.append({
                    'name': product_name,
                    'link': product_link,
                    'specifications': specifications
                })
            else:
                print("Product link not found. Please check the class names.")

        # Print the products with their details
        for product in products:
            print(f"Product Name: {product['name']}")
            print(f"Link: {product['link']}")
            print("Specifications:")
            for key, value in product['specifications'].items():
                print(f"{key}: {value}")
            print("-----------------------------")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
