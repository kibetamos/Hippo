from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

# Set up the Firefox WebDriver
service = Service(executable_path='/usr/bin/geckodriver')  # Update this path
options = Options()
options.headless = True  # Run in headless mode

driver = webdriver.Firefox(service=service, options=options)

def extract_job_listings(url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Find job listings - adjust selector as needed
    job_listings = driver.find_elements(By.CSS_SELECTOR, '.up-card-section')  # Update selector

    for job in job_listings:
        try:
            title = job.find_element(By.CSS_SELECTOR, 'h4').text  # Update selector
            company = job.find_element(By.CSS_SELECTOR, '.up-job-title').text  # Update selector
            location = job.find_element(By.CSS_SELECTOR, '.up-job-location').text  # Update selector
            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print("-" * 40)
        except Exception as e:
            print(f"Error extracting job details: {e}")

    driver.quit()

# Use the URL provided
url = 'https://www.upwork.com/nx/search/jobs/?nbs=1&q=google%20ads'
extract_job_listings(url)
