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

    original_price_element = product.find_element(By.CSS_SELECTOR, 'div.strike-special-price .cross_price')
    original_price = original_price_element.text.strip() if original_price_element else 'N/A'

    discount_element = product.find_element(By.CSS_SELECTOR, 'div.strike-special-price .discount-tittle')
    discount = discount_element.text.strip() if discount_element else 'N/A'

    base_price_element = product.find_element(By.CSS_SELECTOR, 'div.strike-base-price .pricedetails:nth-of-type(1) .price')
    base_price = base_price_element.text.strip() if base_price_element else 'N/A'

    gst_element = product.find_element(By.CSS_SELECTOR, 'div.strike-base-price .pricedetails:nth-of-type(2) .price')
    gst = gst_element.text.strip() if gst_element else 'N/A'

    total_price_element = product.find_element(By.CSS_SELECTOR, 'div.strike-base-price .total-price.price')
    total_price = total_price_element.text.strip() if total_price_element else 'N/A'

    # Collect and store details
    product_details.append({
        'name': name,
        'url': url,
        'price': price,
        'original_price': original_price,
        'discount': discount,
        'base_price': base_price,
        'gst': gst,
        'total_price': total_price
    })

# Print collected product details
for detail in product_details:
    print(f"Name: {detail['name']}")
    print(f"URL: {detail['url']}")
    print(f"Price: {detail['price']}")
    print(f"Original Price: {detail['original_price']}")
    print(f"Discount: {detail['discount']}")
    print(f"Base Price: {detail['base_price']}")
    print(f"GST: {detail['gst']}")
    print(f"Total Price: {detail['total_price']}")
    print("")

# Close the browser
driver.quit()
