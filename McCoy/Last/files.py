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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(filename='scra.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Firefox options
firefox_options = Options()
# firefox_options.add_argument("--headless")  # Uncomment this to run in headless mode

# Initialize the WebDriver for Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# Function to extract specifications and description from the product detail page
def get_specifications_and_description(url):
    driver.get(url)
    try:
        # Wait for the page to be fully loaded and for the description element to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#description'))
        )
        description_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#description'))
        )
    except TimeoutException:
        logging.error(f"Timeout waiting for description section on URL: {url}")
        return {}, {}, None
    except NoSuchElementException:
        logging.error(f"Description section not found on URL: {url}")
        return {}, {}, None

    specs = {}
    description = {
        'Product Description': '',
        'Key Features': '',
        'Benefit & Advantages': '',
        'Surface Preparation': '',
        'Applications': ''
    }
    price_per_piece = None
    
    try:
        # Extract specifications
        spec_elements = driver.find_elements(By.CSS_SELECTOR, '.table-Specifications tr')
        for spec in spec_elements:
            key_element = spec.find_element(By.CSS_SELECTOR, 'td b')
            key = key_element.text.strip() if key_element else None
            value_element = spec.find_elements(By.CSS_SELECTOR, 'td a')
            value = value_element[0].text.strip() if value_element else spec.find_elements(By.CSS_SELECTOR, 'td')[1].text.strip()
            specs[key] = value
    except Exception as e:
        logging.error(f"Error extracting specifications: {e}")
    
    try:
        # Extract product description sections
        description_div = description_element
        description_elements = description_div.find_elements(By.XPATH, './/*')
        current_heading = None

        for elem in description_elements:
            if elem.tag_name == 'h2':
                current_heading = elem.text.strip()
                if current_heading not in description:
                    description[current_heading] = ''
            elif elem.tag_name == 'p':
                if elem.find_elements(By.TAG_NAME, 'strong'):
                    current_heading = elem.find_element(By.TAG_NAME, 'strong').text.strip()
                    if current_heading not in description:
                        description[current_heading] = ''
                elif elem.text.strip():
                    if current_heading:
                        description[current_heading] += elem.text.strip() + ' '
            elif elem.tag_name == 'ul':
                if current_heading:
                    description[current_heading] += '\n'.join([li.text.strip() for li in elem.find_elements(By.TAG_NAME, 'li')]) + ' '
    except Exception as e:
        logging.error(f"Error extracting description: {e}")

    try:
        # Extract price per piece
        price_per_piece = driver.find_element(By.CSS_SELECTOR, '.price-pcs-pdp').text.strip()
    except Exception as e:
        logging.error(f"Error extracting price per piece: {e}")

    return specs, description, price_per_piece

# Function to extract the breadcrumb path
def get_breadcrumb_path():
    try:
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, 'ol.d-flex li')
        path = ' > '.join([element.text.strip() for element in breadcrumb_elements if element.text.strip()])
    except Exception as e:
        logging.error(f"Error extracting breadcrumb path: {e}")
        path = None
    return path

# Read URLs from the text file
def read_urls_from_file(filename):
    urls = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            if len(parts) == 2:
                name_part = parts[0].split(': ', 1)[1]
                url_part = parts[1].split(': ', 1)[1]
                urls.append((name_part, url_part))
    return urls

# Read the URLs from the text file
urls = read_urls_from_file('extracted_data.txt')

# Extract product details and links
products = []

# Limit to 5 items for testing
for i, (name, link) in enumerate(urls):
    driver.get(link)
    time.sleep(10)  # Wait for the page to be fully loaded
    
    product_info = {'Name': name, 'Link': link, 'Status': 'Failed'}

    try:
        title = driver.find_element(By.CSS_SELECTOR, '.item_title_global h4').text.strip()
        product_info['Title'] = title
    except Exception as e:
        logging.error(f"Error extracting title: {e}")
    
    try:
        price = driver.find_element(By.CSS_SELECTOR, '.price_discountarea .price').text.strip()
        product_info['Price'] = price
    except Exception as e:
        logging.error(f"Error extracting price: {e}")

    try:
        old_price = driver.find_element(By.CSS_SELECTOR, '.cross_price').text.strip()
        product_info['Old Price'] = old_price
    except Exception as e:
        logging.error(f"Error extracting old price: {e}")

    try:
        discount_element = driver.find_element(By.CSS_SELECTOR, '.discount-tittle').text.strip()
        discount = discount_element.replace(' OFF', '').strip()
        product_info['Discount'] = discount
    except Exception as e:
        logging.error(f"Error extracting discount: {e}")
    
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

    # Extract specifications, description, price per piece, and breadcrumb path
    try:
        specifications, description, price_per_piece = get_specifications_and_description(link)
        product_info.update({
            'Product Description': description.get('Product Description', '').strip(),
            'Key Features': description.get('Key Features', '').strip(),
            'Benefit & Advantages': description.get('Benefit & Advantages', '').strip(),
            'Surface Preparation': description.get('Surface Preparation', '').strip(),
            'Applications': description.get('Applications', '').strip(),
            'Price Per Piece': price_per_piece,
            'Path': get_breadcrumb_path()
        })
        product_info.update(specifications)
        product_info['Status'] = 'Success'
    except Exception as e:
        logging.error(f"Error extracting product details: {e}")

    products.append(product_info)
    
    # Wait before processing the next item
    time.sleep(5)  # Adjust the time as needed

# Close the driver
driver.quit()

# Convert the data to a DataFrame and save to Excel
df = pd.DataFrame(products)
df.to_excel('Ds.xlsx', index=False)

print("Ds.xlsx")
