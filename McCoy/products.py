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

# Function to extract specifications from the product detail page
def get_specifications(url):
    driver.get(url)
    try:
        # Wait until the specifications table is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-Specifications'))
        )
        specs = {}
        spec_elements = driver.find_elements(By.CSS_SELECTOR, '.table-Specifications tr')
        for spec in spec_elements:
            key_element = spec.find_element(By.CSS_SELECTOR, 'td b')
            key = key_element.text if key_element else None
            value_element = spec.find_elements(By.CSS_SELECTOR, 'td a')
            value = value_element[0].text if value_element else spec.find_elements(By.CSS_SELECTOR, 'td')[1].text
            specs[key] = value
    except Exception as e:
        print(f"Error extracting specifications: {e}")
        specs = None
    return specs

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

# Extract product details and links
products = []
product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards')

for product_item in product_elements:
    try:
        title = product_item.find_element(By.CSS_SELECTOR, '.item_title_global h4').text
    except:
        title = None

    try:
        price = product_item.find_element(By.CSS_SELECTOR, '.price_discountarea .price').text
    except:
        price = None

    try:
        old_price = product_item.find_element(By.CSS_SELECTOR, '.cross_price').text
    except:
        old_price = None

    try:
        discount = product_item.find_element(By.CSS_SELECTOR, '.discount-tittle').text
    except:
        discount = None

    try:
        link = product_item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    except:
        link = None

    # Extract brand information
    try:
        brand_element = product_item.find_element(By.CSS_SELECTOR, '.yale-wrapper a')
        brand_name = brand_element.text
        brand_url = brand_element.get_attribute('href')
    except:
        brand_name = None
        brand_url = None

    # Extract specifications by visiting the product link
    if link:
        specifications = get_specifications(link)
    else:
        specifications = None

    products.append({
        'Title': title,
        'Price': price,
        'Old Price': old_price,
        'Discount': discount,
        'Link': link,
        'Brand Name': brand_name,
        'Brand URL': brand_url,
        'Specifications': specifications
    })

# Close the driver
driver.quit()

# Convert the data to a DataFrame and save to Excel
df = pd.DataFrame(products)
df.to_excel('products_with_brands_and_specs.xlsx', index=False)

print("Data has been saved to products_with_brands_and_specs.xlsx")
