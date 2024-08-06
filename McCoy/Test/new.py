from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
service = Service('/path/to/chromedriver')  # Update path to your WebDriver

driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the product page
url = "https://mccoymart.com/buy/milano-m-30-red-concrete-interlocking-paver-tiles-60-mm/"

def fetch_product_details(url):
    driver.get(url)
    
    # Wait for the page to fully load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.products-content-details')))

    # Breadcrumb Path
    breadcrumb = driver.find_element(By.CSS_SELECTOR, '.breadcrumbs ol')
    breadcrumb_paths = [li.text.strip() for li in breadcrumb.find_elements(By.TAG_NAME, 'li')]

    # Product Images
    images = [img.get_attribute('src') for img in driver.find_elements(By.CSS_SELECTOR, '.carousel-item img')]

    # Product Name
    product_name = driver.find_element(By.CSS_SELECTOR, '.products-content-details').text.strip()

    # Brand
    brand = driver.find_element(By.CSS_SELECTOR, '.yale').text.strip()

    # Price Details
    price_details = {
        'base_price': driver.find_element(By.CSS_SELECTOR, '.baseprice span').text.strip(),
        'discount_price': driver.find_element(By.CSS_SELECTOR, '.discount-price-pdp .price').text.strip(),
        'MRP': driver.find_element(By.CSS_SELECTOR, '.discount-price-pdp strike').text.strip(),
        'total_price': driver.find_element(By.CSS_SELECTOR, '.total-price').text.strip(),
        'GST': driver.find_element(By.CSS_SELECTOR, '.pricedetails:contains("GST") span').text.strip(),
        'inclusive_of_taxes': driver.find_element(By.CSS_SELECTOR, '.included-texes-pdp').text.strip(),
    }

    # Key Features
    features = [li.text.strip() for li in driver.find_elements(By.CSS_SELECTOR, '.key-Features-cnt li')]

    # Availability & Coupons
    availability = driver.find_element(By.CSS_SELECTOR, '.check-availbility-wrapper').text.strip()
    coupons = [div.text.strip() for div in driver.find_elements(By.CSS_SELECTOR, '.apply-coupon-pdp .carousel-item')]

    # Creating a DataFrame
    data = {
        'Breadcrumb Path': breadcrumb_paths,
        'Product Name': product_name,
        'Brand': brand,
        'Images': images,
        'Price Details': [price_details],
        'Key Features': features,
        'Availability': availability,
        'Coupons': coupons
    }

    df = pd.DataFrame([data])
    
    return df

# Fetch details and save to Excel
df = fetch_product_details(url)
print(df)
df.to_excel('product_details.xlsx', index=False)

# Close the WebDriver
driver.quit()
