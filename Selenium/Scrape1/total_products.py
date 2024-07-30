import requests
from bs4 import BeautifulSoup

# URL of the site to scrape
url = "https://www.hippostores.com/k-/productlist?sort=relevance"

# Function to scrape product details
def scrape_products(url):
    # Send a GET request to the website
    response = requests.get(url)

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
                name_tag = product.find('div', class_='productCardRevamped_productName__aEF8u')
                price_tag = product.find('div', class_='productCardRevamped_price__cWkdn')
                mrp_tag = product.find('span', class_='productCardRevamped_mrpPrice__Yz_Yd')
                discount_tag = product.find('div', class_='productCardRevamped_discount__GSjgY')
                link_tag = product.find_parent('a', href=True)  # Assuming the link is in a parent 'a' tag

                if name_tag and price_tag and link_tag:
                    name = name_tag.text.strip()
                    price = price_tag.text.strip()
                    mrp = mrp_tag.text.strip() if mrp_tag else "N/A"
                    discount = discount_tag.text.strip() if discount_tag else "N/A"
                    link = link_tag['href']
                    products.append({'name': name, 'price': price, 'mrp': mrp, 'discount': discount, 'link': link})
                else:
                    print("Product title, price tag, or link not found. Please check the class names.")

            # Print the number of products scraped
            print(f"Number of products scraped: {len(products)}")

            # Return the list of products
            return products
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Function to get total number of products displayed
def get_total_products(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract total number of products displayed
        result_info = soup.find('div', class_='jss36')

        if result_info:
            products_text = result_info.text.strip()
            total_products = int(products_text.split('|')[-1].strip().split()[0])
            return total_products
        else:
            print("Could not find the product count information.")
            return None
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Main script execution
if __name__ == "__main__":
    # Scrape products
    scraped_products = scrape_products(url)

    if scraped_products:
        # Get total number of products
        total_products = get_total_products(url)

        if total_products is not None:
            print(f"Total number of products: {total_products}")

            # Compare the number of products scraped with total products
            if len(scraped_products) == total_products:
                print("Number of scraped products matches total products displayed.")
            else:
                print("Number of scraped products does not match total products displayed.")
        else:
            print("Failed to retrieve total number of products.")
    else:
        print("No products scraped. Check previous errors.")
