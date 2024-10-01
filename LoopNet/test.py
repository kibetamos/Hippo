from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver for Firefox
driver = webdriver.Firefox()

# Base URL for the LoopNet brokers in Nashville
base_url = "https://www.loopnet.com/commercial-real-estate-brokers/tn/nashville/"

total_broker_count = 0

# Loop through page numbers from 1 to 20
for page_num in range(1, 3):  # Pages 1 to 20
    # Construct the URL for each page
    if page_num == 1:
        url = base_url  # First page doesn't have the number
    else:
        url = f"{base_url}{page_num}/"  # Subsequent pages
    
    driver.get(url)  # Open the URL
    time.sleep(5)  # Wait for the page to load completely
    
    # Find all broker elements using the common class name 'search-result-placard'
    broker_elements = driver.find_elements(By.CLASS_NAME, 'search-result-placard')
    
    # Count the number of brokers on the current page
    broker_count = len(broker_elements)
    total_broker_count += broker_count
    
    # Print the result for the current page
    print(f'There are {broker_count} brokers on page {page_num} ({url}).')

# Print the total broker count across all pages
print(f'Total brokers across all pages: {total_broker_count}')

# Close the browser
driver.quit()
