from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import json
import re

# Setup Firefox options
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode

# Initialize the WebDriver for Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# Navigate to the page
driver.get('https://mccoymart.com/buy/aac-blocks/')

# Extract the heading
heading = driver.find_element(By.CSS_SELECTOR, 'h1.main-heading-title').text
print(f"Heading: {heading}")

# Extract breadcrumbs
breadcrumbs = []
breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, '.breadcrumbs ol li a')
for breadcrumb in breadcrumb_elements:
    breadcrumbs.append({
        'text': breadcrumb.text,
        'url': breadcrumb.get_attribute('href')
    })
print("Breadcrumbs:")
for crumb in breadcrumbs:
    print(crumb)

# Extract structured data (JSON-LD)
scripts = driver.find_elements(By.TAG_NAME, 'script')
structured_data = []
for script in scripts:
    if 'application/ld+json' in script.get_attribute('type'):
        try:
            data = json.loads(script.get_attribute('innerHTML'))
            structured_data.append(data)
        except json.JSONDecodeError:
            pass

# print("Structured Data:")
# for data in structured_data:
#     print(json.dumps(data, indent=2))

# Extract total number of items
items_text = driver.find_element(By.CSS_SELECTOR, '.showing-items .productsnumbers').text
total_items_match = re.search(r'(\d+)', items_text)
total_items = total_items_match.group(1) if total_items_match else None
print(f"Total number of items: {total_items}")

# Extract products
products = []
product_elements = driver.find_elements(By.CSS_SELECTOR, '.product-item')  # Adjust selector as needed
for product_item in product_elements:
    title = product_item.find_element(By.CSS_SELECTOR, '.product-title').text if product_item.find_element(By.CSS_SELECTOR, '.product-title') else None
    price = product_item.find_element(By.CSS_SELECTOR, '.product-price').text if product_item.find_element(By.CSS_SELECTOR, '.product-price') else None
    link = product_item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') if product_item.find_element(By.CSS_SELECTOR, 'a') else None
    products.append({
        'title': title,
        'price': price,
        'link': link,
    })

print("Products:")
for product in products:
    print(product)

# Close the
