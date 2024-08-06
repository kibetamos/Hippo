from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

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

# Close the browser
driver.quit()
