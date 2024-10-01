from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Set up the WebDriver for Firefox
driver = webdriver.Firefox()

# Open the LoopNet brokers page (single page)
url = "https://www.loopnet.com/commercial-real-estate-brokers/tn/nashville/"
driver.get(url)
time.sleep(5)  # Wait for the page to load completely

# Find all broker elements using the class name 'search-result-placard'
broker_elements = driver.find_elements(By.CLASS_NAME, 'search-result-placard')

# Open a CSV file to write the broker data
with open('brokers_nashville.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(['First Name', 'Last Name', 'Job Title', 'Company', 'Location', 'Phone Number', 'Email Available', 'Profile Link', 'Photo URL'])

    # Extract and write data for each broker
    for broker_element in broker_elements:
        # Name
        name_element = broker_element.find_element(By.XPATH, './/h4/a')
        full_name = name_element.text
        first_name, last_name = full_name.split(' ', 1)

        # Job Title
        title_element = broker_element.find_element(By.XPATH, './/p[@class="broker-oneline"]')
        job_title = title_element.text

        # Company
        company_element = broker_element.find_element(By.XPATH, './/span[@class="company"]')
        company_name = company_element.text

        # Location
        location_element = broker_element.find_element(By.XPATH, './/span[@class="location"]')
        location = location_element.text

        # Phone Number
        phone_element = broker_element.find_element(By.XPATH, './/p[@class="contact-number"]')
        phone_number = phone_element.text.strip()

        # Email (check if present)
        email_exists = "No"
        try:
            email_element = broker_element.find_element(By.XPATH, './/a[@class="broker-email"]')
            email_exists = "Yes"
        except:
            pass  # No email link available

        # Profile Link
        profile_link = name_element.get_attribute('href')

        # Photo URL
        photo_element = broker_element.find_element(By.XPATH, './/div[@class="broker-photo"]//img')
        photo_url = photo_element.get_attribute('src')

        # Write broker data to the CSV file
        writer.writerow([first_name, last_name, job_title, company_name, location, phone_number, email_exists, profile_link, photo_url])

# Close the browser
driver.quit()

print('Data saved to brokers_nashville.csv')
