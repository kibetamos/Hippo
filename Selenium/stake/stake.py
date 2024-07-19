from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to GeckoDriver
driver_path = '/usr/bin/geckodriver'
service = Service(driver_path)

# Initialize the Firefox WebDriver
driver = webdriver.Firefox(service=service)

try:
    # Navigate to Stake.com
    driver.get("https://stake.com/")

    # Wait for the user to manually complete the human verification
    input("Please complete the human verification and press Enter to continue...")

    # Wait for the table to be visible
    table = WebDriverWait(driver, 90).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'table-content'))
    )

    # Extract the header
    headers = [header.text for header in table.find_elements(By.XPATH, './/thead/tr/th')]

    # Extract the rows
    rows = table.find_elements(By.XPATH, './/tbody/tr')

    # Extract the data from each row
    data = []
    for row in rows:
        cells = row.find_elements(By.XPATH, './/td')
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    # Print the extracted data
    print(headers)
    for row in data:
        print(row)

finally:
    # Close the browser
    driver.quit()
