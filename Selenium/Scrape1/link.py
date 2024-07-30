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
    print(f"Processing link: {link}")
    # You can implement the rest of the function here

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

                fetch_product_description_and_sku(full_link)
            else:
                print("Product link not found. Please check the class names.")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
