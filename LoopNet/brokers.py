from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Function to scrape broker data from the current page
def scrape_brokers_from_page(writer):
    # Find all broker elements using the class name 'search-result-placard'
    broker_elements = driver.find_elements(By.CLASS_NAME, 'search-result-placard')

    # Extract and write data for each broker
    for broker_element in broker_elements:
        try:
            # Name (First and Last)
            name_element = broker_element.find_element(By.XPATH, './/h4/a')
            full_name = name_element.text
            first_name, last_name = full_name.split(' ', 1)

            # Phone Number
            phone_element = broker_element.find_element(By.XPATH, './/p[@class="contact-number"]')
            phone_number = phone_element.text.strip()

            # Write broker data to the CSV file
            writer.writerow([first_name, last_name, phone_number])
        except Exception as e:
            print(f"Error processing broker: {e}")

# Set up the WebDriver for Firefox
driver = webdriver.Firefox()

# Open a CSV file to write the broker data
with open('brokers_nashville.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(['First Name', 'Last Name', 'Phone Number'])

    # Loop through pages 1 to 20
    for page in range(1, 53):  # 1 to 20
        # Construct the URL for the current page
        url = f"https://www.loopnet.com/commercial-real-estate-brokers/tn/nashville/{page}/" if page > 1 else "https://www.loopnet.com/commercial-real-estate-brokers/tn/nashville/"
        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely

        # Scrape the data on the current page
        scrape_brokers_from_page(writer)

# Close the browser
driver.quit()

print('Data saved to brokers_nashville.csv')
