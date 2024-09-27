import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Initialize Selenium WebDriver (Here I'm using Chrome, adjust for Firefox or others)
driver = webdriver.Chrome()

# Open the website
url = 'https://materialdepot.in/'
driver.get(url)

# Wait for page to fully load
time.sleep(5)  # Adjust sleep time as necessary to ensure the page is loaded

# Get the page source
page_source = driver.page_source

# Close the Selenium driver
driver.quit()

# Parse the page with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Example: Extract product names and prices (customize for actual structure of the site)
products = []
for product in soup.find_all('div', class_='product-item'):  # Adjust the class based on the website's structure
    name = product.find('h2').text if product.find('h2') else 'No name'
    price = product.find('span', class_='price').text if product.find('span', class_='price') else 'No price'
    products.append({'Name': name, 'Price': price})

# Convert to a DataFrame
df = pd.DataFrame(products)

# Save the scraped data to an Excel file
df.to_excel('scraped_materialdepot_products.xlsx', index=False)

print('Scraping complete! Data saved to "scraped_materialdepot_products.xlsx"')
