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
    description = ""

    try:
        # Wait until the description heading is present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.description-title-pdp'))
        )

        # Locate the description text
        description_element = driver.find_element(By.CSS_SELECTOR, '.products-description-pdp')
        paragraphs = description_element.find_elements(By.TAG_NAME, 'p')

        for para in paragraphs:
            description += para.text + "\n"
    except Exception as e:
        print(f"Error extracting description: {e}")

    try:
        # Extract specifications if available
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-Specifications'))
        )
        spec_elements = driver.find_elements(By.CSS_SELECTOR, '.table-Specifications tr')
        for spec in spec_elements:
            try:
                key_element = spec.find_element(By.CSS_SELECTOR, 'td b')
                key = key_element.text.strip()
            except:
                key = None

            try:
                value_elements = spec.find_elements(By.CSS_SELECTOR, 'td')
                value = value_elements[1].text.strip() if len(value_elements) > 1 else None
            except:
                value = None

            if key and value:
                specs[key] = value
    except Exception as e:
        print(f"Error extracting specifications: {e}")

    return specs, description

# Function to extract breadcrumb path
def get_breadcrumb_path():
    try:
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, '.d-flex.pl-0 li a')
        breadcrumb_path = ' > '.join([breadcrumb.text.strip() for breadcrumb in breadcrumb_elements])
        return breadcrumb_path
    except Exception as e:
        print(f"Error extracting breadcrumb path: {e}")
        return None

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
product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards')
product_links = []

for product_item in product_elements:
    try:
        link = product_item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        product_links.append(link)
    except Exception as e:
        print(f"Error extracting link: {e}")

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
        discount = driver.find_element(By.CSS_SELECTOR, '.discount-tittle').text.strip()
    except:
        discount = None

    # Extract specifications, description, and breadcrumb path
    specifications, description = get_specifications_and_description(link)
    path = get_breadcrumb_path()

    # Combine all extracted data into a single dictionary
    product_info = {
        'Title': title,
        'Price': price,
        'Old Price': old_price,
        'Discount': discount,
        'Link': link,
        'Description': description,
        'Path': path
    }

    # Add specifications to the product info
    product_info.update(specifications)

    products.append(product_info)

# Close the driver
driver.quit()

# Convert the data to a DataFrame and save to Excel
df = pd.DataFrame(products)
df.to_excel('products_path.xlsx', index=False)

print("Data has been saved to products_with_brands_specs_description_and_path.xlsx")
