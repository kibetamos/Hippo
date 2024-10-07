from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Function to scrape product data from the current page
def scrape_products_from_page(writer):
    # Find all product elements
    product_elements = driver.find_elements(By.CLASS_NAME, 'product-item')

    # Check if products are found
    if len(product_elements) == 0:
        print("No products found on this page.")
    else:
        print(f"Found {len(product_elements)} products on this page.")

    # Extract and write data for each product
    for product_element in product_elements:
        try:
            # Product Name
            name_element = product_element.find_element(By.CLASS_NAME, 'product-title')
            product_name = name_element.text.strip()

            # Product Price (if available)
            try:
                price_element = product_element.find_element(By.CLASS_NAME, 'price')
                product_price = price_element.text.strip()
            except:
                product_price = 'N/A'  # If price is not available

            # Print product details to verify
            print(f"Product: {product_name}, Price: {product_price}")

            # Write product data to the CSV file
            writer.writerow([product_name, product_price])
        except Exception as e:
            print(f"Error processing product: {e}")

# Set up the WebDriver for Firefox
driver = webdriver.Firefox()

# Open a CSV file to write the product data
with open('products_materialdepot.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(['Product Name', 'Product Price'])

    # Loop through pages 1 to 5 (you can extend the range as needed)
    for page in range(1, 6):  # 1 to 5
        # Construct the URL with a similar pattern as LoopNet
        url = f"https://materialdepot.in/kitchen-decorative-laminates?handle=kitchen-decorative-laminates&page={page}" if page > 1 else "https://materialdepot.in/kitchen-decorative-laminates?handle=kitchen-decorative-laminates"
        
        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely

        # Scrape the data on the current page
        print(f"Scraping data from page {page}...")
        scrape_products_from_page(writer)

# Close the browser
driver.quit()

print('Data saved to products_materialdepot.csv')
