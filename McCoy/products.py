from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

# Setup Firefox options
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode

# Initialize the WebDriver for Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# Navigate to the page
driver.get('https://mccoymart.com/buy/aac-blocks/')

# Extract product details
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

    try:
        brand_element = product_item.find_element(By.CSS_SELECTOR, '.yale-wrapper a')
        brand_name = brand_element.text
        brand_url = brand_element.get_attribute('href')
    except:
        brand_name = None
        brand_url = None

    # Extract specifications
    try:
        spec_elements = product_item.find_elements(By.CSS_SELECTOR, '.table-Specifications tr')
        specifications = {}
        for spec in spec_elements:
            key = spec.find_element(By.CSS_SELECTOR, 'td b').text
            value_element = spec.find_elements(By.CSS_SELECTOR, 'td a')
            value = value_element[0].text if value_element else spec.find_elements(By.CSS_SELECTOR, 'td')[1].text
            specifications[key] = value
    except:
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
