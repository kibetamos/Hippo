from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome WebDriver
options = Options()
options.headless = False  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Access the page
url = "https://www.upwork.com/freelancers/~0119aa583aa4d723c4"
driver.get(url)

# Allow some time for the page to load
time.sleep(5)

# Example: Extract the profile name
profile_name = driver.find_element(By.CSS_SELECTOR, "selector-for-profile-name").text
print(f"Profile Name: {profile_name}")

# Close the driver
driver.quit()
