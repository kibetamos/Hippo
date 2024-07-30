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
            brand_tag = product.find('div', class_='productCardRevamped_brandContainer__1mgym')
            model_tag = product.find('div', class_='productCardRevamped_modelContainer__FgPRb')
            link_tag = product.find_parent('a', href=True)  # Assuming the link is in a parent 'a' tag

            if name_tag and price_tag and link_tag:
                name = name_tag.text.strip()
                price = price_tag.text.strip()
                mrp = mrp_tag.text.strip() if mrp_tag else "N/A"
                discount = discount_tag.text.strip() if discount_tag else "N/A"
                brand = brand_tag.text.strip() if brand_tag else "N/A"
                model = model_tag.text.strip() if model_tag else "N/A"
                link = link_tag['href']

                # Prepend the base URL if the link is relative
                full_link = 'https://www.hippostores.com' + link if not link.startswith('https://') else link
                
                products.append({
                    'name': name,
                    'price': price,
                    'mrp': mrp,
                    'discount': discount,
                    'brand': brand,
                    'model': model,
                    'link': full_link
                })
            else:
                print("Product title, price tag, or link not found. Please check the class names.")

        # Number of products
        num_products = len(products)
        print(f"Number of products: {num_products}")

        # Print the products
        for product in products:
            print(f"Name: {product['name']}, Price: {product['price']}, MRP: {product['mrp']}, Discount: {product['discount']}, Brand: {product['brand']}, Model: {product['model']}, Link: {product['link']}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
