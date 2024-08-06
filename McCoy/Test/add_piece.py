from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time

# Setup Firefox options
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode

# Initialize the WebDriver for Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# Function to extract specifications and description from the product detail page
def get_specifications_and_description(url):
    driver.get(url)
    time.sleep(10)  # Wait for the page to be fully loaded
    specs = {}
    description = {}
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
            value_element = spec.find_elements(By.CSS_SELECTOR, 'td a')
            value = value_element[0].text.strip() if value_element else spec.find_elements(By.CSS_SELECTOR, 'td')[1].text.strip()
            specs[key] = value
    except Exception as e:
        print(f"Error extracting specifications: {e}")
    
    try:
        # Extract product description sections
        description_sections = driver.find_elements(By.CSS_SELECTOR, '#description p, #description ul')
        for section in description_sections:
            if section.tag_name == 'p' and section.text.strip():
                key = "Description"
                value = section.text.strip()
            elif section.tag_name == 'ul':
                key = "Features"
                value = '\n'.join([li.text.strip() for li in section.find_elements(By.TAG_NAME, 'li')])
            else:
                continue
            description[key] = value
    except Exception as e:
        print(f"Error extracting description: {e}")

    try:
        # Extract price per piece
        price_per_piece = driver.find_element(By.CSS_SELECTOR, '.price-pcs-pdp').text.strip()
    except Exception as e:
        print(f"Error extracting price per piece: {e}")

    return specs, description, price_per_piece

# Function to extract the breadcrumb path
def get_breadcrumb_path():
    try:
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, 'ol.d-flex li')
        path = ' > '.join([element.text.strip() for element in breadcrumb_elements if element.text.strip()])
    except Exception as e:
        print(f"Error extracting breadcrumb path: {e}")
        path = None
    return path

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

# Navigate to the main page
driver.get('https://mccoymart.com/buy/aac-blocks/')

# Scroll the page to load all products
scroll_to_bottom()

# Extract product links
product_links = [product.get_attribute('href') for product in driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')]

# Extract product details and links
products = []

for link in product_links:
    driver.get(link)
    time.sleep(10)  # Wait for the page to be fully loaded
    
    try:
        title = driver.find_element(By.CSS_SELECTOR, '.item_title_global h4').text.strip()
    except:
        title = None

    try:
        price = driver.find_element(By.CSS_SELECTOR, '.price_discountarea .price').text.strip()
    except:
        price = None

    try:
        old_price = driver.find_element(By.CSS_SELECTOR, '.cross_price').text.strip()
    except:
        old_price = None

    try:
        discount_element = driver.find_element(By.CSS_SELECTOR, '.discount-tittle').text.strip()
        discount = discount_element.replace(' OFF', '').strip()
    except:
        discount = None
    
    try:
        pack_price_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityAmount')
        pack_price = pack_price_element.text.strip()
    except:
        pack_price = None

    try:
        quantity_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityPcs')
        quantity = quantity_element.text.strip()
    except:
        quantity = None

    # Extract specifications, description, price per piece, and breadcrumb path
    specifications, description, price_per_piece = get_specifications_and_description(link)
    path = get_breadcrumb_path()

    # Combine all extracted data into a single dictionary
    product_info = {
        'Title': title,
        'Price': price,
        'Old Price': old_price,
        'Discount': discount,
        'Link': link,
        'Description': description.get('Description'),
        'Features': description.get('Features'),
        'Path': path,
        'Price Per Piece': price_per_piece,
        'Pack Price': pack_price,
        'Quantity': quantity
    }

    # Add specifications to the product info
    product_info.update(specifications)

    products.append(product_info)

# Close the driver
driver.quit()

# Convert the data to a DataFrame and save to Excel
df = pd.DataFrame(products)
df.to_excel('products_with_path.xlsx', index=False)

print("Data_path.xlsx")
