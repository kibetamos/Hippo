import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time

# Setup logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Firefox options
firefox_options = Options()
# firefox_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize the WebDriver for Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# Function to scroll to the bottom of the page and wait for all products to load
def load_all_products():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for page to load and allow time for additional content
        time.sleep(10)  # Adjust time as needed to ensure all content is loaded
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to extract product details from the page
def extract_product_details():
    products = []
    # Extract product elements
    product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')
    product_links = [product.get_attribute('href') for product in product_elements]
    unique_links = set(product_links)
    
    # Process each product link
    for i, link in enumerate(unique_links):
        driver.get(link)
        time.sleep(10)  # Wait for the page to be fully loaded

        # Scroll until the product description section is in view
        scroll_until_description_in_view('#description')
        
        product_info = {'Link': link, 'Status': 'Failed'}

        try:
            title = driver.find_element(By.CSS_SELECTOR, '.products-content-details').text
            product_info['Title'] = title
        except Exception as e:
            logging.error(f"Error extracting title for product {link}: {e}")

        try:
            pack_price_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityAmount')
            pack_price = pack_price_element.text
            product_info['Pack Price'] = pack_price
        except Exception as e:
            logging.error(f"Error extracting pack price for product {link}: {e}")

        try:
            quantity_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityPcs')
            quantity = quantity_element.text
            product_info['Quantity'] = quantity
        except Exception as e:
            logging.error(f"Error extracting quantity for product {link}: {e}")

        try:
            specs, description, price_per_piece, mrp, discount, tax, rating, rating_value = get_specifications_and_description(link)
            breadcrumb_path = get_breadcrumb_path()
            product_info.update({
                'MRP': mrp,
                'Pack Price': pack_price,
                'Discount': discount,
                'Tax': tax,
                'Price Per Piece': price_per_piece,
                'Quantity': quantity,
                'Product Description': description.get('Product Description', ''),
                'Status': 'Success'
            })
            product_info.update(specs)
            product_info.update(breadcrumb_path)
        except Exception as e:
            logging.error(f"Error extracting product details for product {link}: {e}")

        products.append(product_info)

    return products

# Function to handle the scraping of each shop from the shops.txt file
def scrape_shops(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    all_products = []
    
    for line in lines:
        name, url = line.strip().split(', URL: ')
        logging.info(f'Scraping shop: {name}, URL: {url}')
        
        driver.get(url)
        load_all_products()
        products = extract_product_details()
        all_products.extend(products)
    
    driver.quit()
    
    # Create a DataFrame from the list of products
    df = pd.DataFrame(all_products)

    # Group by the first category
    grouped_df = df.groupby('Category 1')

    # Create an Excel writer object and save each group to a separate sheet
    try:
        with pd.ExcelWriter('sample5.xlsx', engine='openpyxl') as writer:
            for category, group in grouped_df:
                safe_category = str(category).replace('/', '_').replace('\\', '_')
                group.to_excel(writer, sheet_name=safe_category, index=False)
    except Exception as e:
        logging.error(f"Error saving to Excel: {e}")

# Run the scraper
scrape_shops('shops.txt')
