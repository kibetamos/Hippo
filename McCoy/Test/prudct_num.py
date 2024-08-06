import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time
import re

# Setup logging
logging.basicConfig(filename='scrape.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Firefox options
firefox_options = Options()
# firefox_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize the WebDriver for Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for page to load
        time.sleep(5)  # Increased wait time
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to extract product count from the page
def extract_product_count():
    try:
        count_element = driver.find_element(By.CSS_SELECTOR, '.showing-items .productsnumbers')
        count_text = count_element.text.strip()
        # Extract the total number of items using regex
        match = re.search(r'(\d+)', count_text)
        if match:
            total_products = int(match.group(1))
            logging.info(f"Total number of products found: {total_products}")
            return total_products
        else:
            logging.error("Total number of products not found in the text.")
            return None
    except Exception as e:
        logging.error(f"Error extracting product count: {e}")
        return None

# Function to extract product links from the page
def get_product_links():
    try:
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')
        return [product.get_attribute('href') for product in product_elements]
    except Exception as e:
        logging.error(f"Error extracting product links: {e}")
        return []

# Function to extract specifications and description from the product detail page
def get_specifications_and_description(url):
    driver.get(url)
    time.sleep(10)  # Wait for the page to be fully loaded

    specs = {}
    description = {
        'Product Description': '',
        'Key Features': '',
        'Benefit & Advantages': '',
        'Surface Preparation': '',
        'Applications': ''
    }
    price_per_piece = None
    mrp = None
    discount = None

    try:
        # Extract specifications
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-Specifications'))
        )
        spec_elements = driver.find_elements(By.CSS_SELECTOR, '.table-Specifications tr')
        for spec in spec_elements:
            key_element = spec.find_element(By.CSS_SELECTOR, 'td b')
            key = key_element.text.strip() if key_element else None
            value_elements = spec.find_elements(By.CSS_SELECTOR, 'td')
            value = value_elements[1].text.strip() if len(value_elements) > 1 else ''
            if key:
                specs[key] = value
    except Exception as e:
        logging.error(f"Error extracting specifications: {e}")

    try:
        # Extract product description sections
        description_div = driver.find_element(By.CSS_SELECTOR, '#description')
        description_elements = description_div.find_elements(By.XPATH, './/*')
        current_heading = None
        content = []

        for elem in description_elements:
            if elem.tag_name == 'h2':
                if current_heading:
                    description[current_heading] = '\n'.join(content).strip()
                current_heading = elem.text.strip()
                content = []
                if current_heading not in description:
                    description[current_heading] = ''
            elif elem.tag_name == 'p':
                content.append(elem.text.strip())
            elif elem.tag_name == 'ul':
                items = [li.text.strip() for li in elem.find_elements(By.TAG_NAME, 'li')]
                content.append('\n'.join(items))

        if current_heading:
            description[current_heading] = '\n'.join(content).strip()
    
    except Exception as e:
        logging.error(f"Error extracting description: {e}")

    try:
        # Extract price per piece
        price_per_piece_element = driver.find_element(By.CSS_SELECTOR, '.price-pcs-pdp')
        price_per_piece = price_per_piece_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting price per piece: {e}")

    try:
        # Extract MRP
        mrp_element = driver.find_element(By.CSS_SELECTOR, '.discount-price-pdp strike')
        mrp = mrp_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting MRP: {e}")

    try:
        # Extract discount percentage
        discount_element = driver.find_element(By.CSS_SELECTOR, '.off-price-pdp')
        discount = discount_element.text.strip().replace('off', '').strip()
    except Exception as e:
        logging.error(f"Error extracting discount: {e}")

    return specs, description, price_per_piece, mrp, discount

# Function to extract the breadcrumb path and split into categories
def get_breadcrumb_path():
    try:
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, 'ol.d-flex li')
        # Extract the text from each breadcrumb element
        path_list = [element.text.strip() for element in breadcrumb_elements if element.text.strip()]
        # Combine the path into a single string
        full_path = ' > '.join(path_list)
    except Exception as e:
        logging.error(f"Error extracting breadcrumb path: {e}")
        path_list = []
        full_path = ''
    
    # Create a dictionary to store categories with dynamic column names
    path_dict = {f'Category {i+1}': path_list[i] for i in range(len(path_list))}
    return full_path, path_dict

# Measure the time to load the first 10 products
start_time = time.time()

# Navigate to the main page
driver.get('https://mccoymart.com/buy/kitchen-fitting-hardware/')

# Scroll the page to load all products
scroll_to_bottom()

# Extract total number of products
total_products = extract_product_count()

# Extract product links
product_links = get_product_links()

# Limit to the first 10 products
product_links = product_links[:4]

# Extract product details and links
products = []

for link in product_links:
    driver.get(link)
    time.sleep(10)  # Wait for the page to be fully loaded
    
    # Extract product details
    product_info = {'Link': link, 'Status': 'Failed'}

    try:
        title = driver.find_element(By.CSS_SELECTOR, '.item_title_global h4').text.strip()
        product_info['Title'] = title
    except Exception as e:
        logging.error(f"Error extracting title: {e}")

    try:
        pack_price_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityAmount')
        pack_price = pack_price_element.text.strip()
        product_info['Pack Price'] = pack_price
    except Exception as e:
        logging.error(f"Error extracting pack price: {e}")

    try:
        quantity_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityPcs')
        quantity = quantity_element.text.strip()
        product_info['Quantity'] = quantity
    except Exception as e:
        logging.error(f"Error extracting quantity: {e}")

    # Extract specifications, description, price per piece, MRP, discount, and breadcrumb path
    try:
        specifications, description, price_per_piece, mrp, discount = get_specifications_and_description(link)
        full_path, breadcrumb_path = get_breadcrumb_path()
        product_info.update({
            'MRP': mrp if mrp else 'N/A',
            'Pack Price': pack_price if pack_price else 'N/A',
            'Discount': discount if discount else 'N/A',
            'Price Per Piece': price_per_piece if price_per_piece else 'N/A',
            'Quantity': quantity if quantity else 'N/A',
            'Product Description': description.get('Product Description', '').strip(),
            'Key Features': description.get('Key Features', '').strip(),
            'Benefit & Advantages': description.get('Benefit & Advantages', '').strip(),
            'Surface Preparation': description.get('Surface Preparation', '').strip(),
            'Applications': description.get('Applications', '').strip(),
            'Full Breadcrumb Path': full_path,  # New column for the full path
            'Status': 'Success'
        })
        product_info.update(specifications)
        product_info.update(breadcrumb_path)
    except Exception as e:
        logging.error(f"Error extracting product details: {e}")

    products.append(product_info)

end_time = time.time()
elapsed_time = end_time - start_time

# Close the driver
driver.quit()

# Create a DataFrame from the list of products
df = pd.DataFrame(products)

# Save the DataFrame to an Excel file with the desired format
output_file = 'product_details.xlsx'
df.to_excel(output_file, index=False)

# Print the results to console
print(df)
print(f"Time taken to load and process the first 10 products: {elapsed_time:.2f} seconds")
print(f"Results saved to {output_file}")
