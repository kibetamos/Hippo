from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

# Define the proxy (Replace with your Indian proxy)
proxy_ip_port = " 125.99.106.250:3128"  # Example: "192.168.1.1:8080"


# Set up the Proxy object
firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument('--headless')  # Optional: Run in headless mode

# Configure the proxy settings directly in Firefox options
firefox_options.set_preference("network.proxy.type", 1)
firefox_options.set_preference("network.proxy.http", proxy_ip_port.split(':')[0])
firefox_options.set_preference("network.proxy.http_port", int(proxy_ip_port.split(':')[1]))
firefox_options.set_preference("network.proxy.ssl", proxy_ip_port.split(':')[0])
firefox_options.set_preference("network.proxy.ssl_port", int(proxy_ip_port.split(':')[1]))

# Initialize WebDriver with options
driver = webdriver.Firefox(options=firefox_options)

# Load the main page
driver.get('http://www.materialdepot.in/')

# Wait for the page to load
time.sleep(5)

# Continue with your scraping logic...

# Close the browser
driver.quit()