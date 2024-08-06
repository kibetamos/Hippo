from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Path to geckodriver
driver_path = '/usr/bin/geckodriver'

# Set up the Service object with the path to geckodriver
service = Service(driver_path)

# Initialize the Firefox WebDriver using the service
driver = webdriver.Firefox(service=service)

# Load the page
driver.get('https://mccoymart.com/buy/aac-blocks/')

# Wait for 10 seconds to allow data to load
time.sleep(10)

# Scroll down to the bottom of the page to ensure all content is loaded
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for content to load
    time.sleep(2)  # Adjust this value if necessary

    # Calculate new scroll height and compare with last height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all product elements
products = driver.find_elements(By.CSS_SELECTOR, 'div.item.global-card-list.brands-mccoy-cards')

# Collect details of each product
product_details = []

for product in products:
    # Extract product details
    name_element = product.find_element(By.CSS_SELECTOR, 'div.item_title_global h4')
    name = name_element.text.strip() if name_element else 'N/A'

    url_element = product.find_element(By.CSS_SELECTOR, 'a[href]')
    url = url_element.get_attribute('href') if url_element else 'N/A'

    price_element = product.find_element(By.CSS_SELECTOR, 'div.price_discountarea .price')
    price = price_element.text.strip() if price_element else 'N/A'

    # Click on the product link to open the detail page
    product.click()
    
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # Wait for the detail page to load and stay for 10 seconds
    time.sleep(10)

    # Scroll down to the bottom of the page to ensure all content is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Extract manufacturer details and specifications from the detail page
    try:
        # Extract brand (if available)
        brand_element = driver.find_element(By.CSS_SELECTOR, 'a span.yale')
        brand = brand_element.text.strip() if brand_element else 'N/A'
    except Exception as e:
        print(f"Error extracting brand for {name}: {e}")
        brand = 'N/A'

    # Extract specifications
    specifications = {}
    try:
        spec_elements = driver.find_elements(By.CSS_SELECTOR, 'div.specifications-wrapper .specification')
        for spec in spec_elements:
            key = spec.find_element(By.CSS_SELECTOR, 'span.specification-label').text.strip()
            value = spec.find_element(By.CSS_SELECTOR, 'span.specification-value').text.strip()
            specifications[key] = value
    except Exception as e:
        print(f"Error extracting specifications for {name}: {e}")
    
    # Collect and store details
    product_details.append({
        'name': name,
        'url': url,
        'price': price,
        'brand': brand,
        'specifications': specifications
    })

    # Close the detail page tab
    driver.close()

    # Switch back to the main page
    driver.switch_to.window(driver.window_handles[0])

# Print collected product details
for detail in product_details:
    print(f"Name: {detail['name']}")
    print(f"URL: {detail['url']}")
    print(f"Price: {detail['price']}")
    print(f"Brand: {detail['brand']}")
    print(f"Specifications:")
    for key, value in detail['specifications'].items():
        print(f"  {key}: {value}")
    print("")

# Close the browser
driver.quit()
