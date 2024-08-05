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

# Setup logging
logging.basicConfig(filename='scra.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        time.sleep(3)
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to scroll until the product description section is in view
def scroll_until_description_in_view(description_selector):
    while True:
        try:
            # Scroll down to bottom to ensure the page is fully loaded
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for the page to load
            
            # Check if the description section is in view
            description_element = driver.find_element(By.CSS_SELECTOR, description_selector)
            if description_element.is_displayed():
                break
        except Exception as e:
            logging.error(f"Error checking description visibility: {e}")

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

    return specs, description, price_per_piece

# Function to extract the breadcrumb path and split into categories
def get_breadcrumb_path():
    try:
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, 'ol.d-flex li')
        # Extract the text from each breadcrumb element except the last one (product name)
        path_list = [element.text.strip() for element in breadcrumb_elements[:-1] if element.text.strip()]
    except Exception as e:
        logging.error(f"Error extracting breadcrumb path: {e}")
        path_list = []

    # Create a dictionary to store categories with dynamic column names
    path_dict = {f'Category {i+1}': path_list[i] for i in range(len(path_list))}
    return path_dict

# Navigate to the main page
driver.get('https://mccoymart.com/buy/aac-blocks/')

# Scroll the page to load all products
scroll_to_bottom()

# Count number of items on the page
num_items = len(driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards'))
logging.info(f'Number of items found on the page: {num_items}')

# Extract product links
product_links = [product.get_attribute('href') for product in driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')]

# Extract product details and links
products = []

# Limit to the first 5 products
for i, link in enumerate(product_links[:1]):
    driver.get(link)
    time.sleep(10)  # Wait for the page to be fully loaded
    
    # Scroll until the product description section is in view
    scroll_until_description_in_view('#description')
    
    product_info = {'Link': link, 'Status': 'Failed'}

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
        breadcrumb_path = get_breadcrumb_path()
        product_info.update({
            'Product Description': description.get('Product Description', '').strip(),
            'Key Features': description.get('Key Features', '').strip(),
            'Benefit & Advantages': description.get('Benefit & Advantages', '').strip(),
            'Surface Preparation': description.get('Surface Preparation', '').strip(),
            'Applications': description.get('Applications', '').strip(),
            'Price Per Piece': price_per_piece,
            'Status': 'Success'
        })
        product_info.update(specifications)
        product_info.update(breadcrumb_path)
    except Exception as e:
        logging.error(f"Error extracting product details: {e}")

    products.append(product_info)

# Close the driver
driver.quit()

# Convert the data to a DataFrame and save it to Excel
df = pd.DataFrame(products)
df.to_excel('Ds.xlsx', index=False)

print("Ds.xlsx")
