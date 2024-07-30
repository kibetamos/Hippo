from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import logging
import gc
import os

# Setup logging
logging.basicConfig(filename='scraping_hippo_last.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to GeckoDriver
driver_path = '/usr/bin/geckodriver'
service = Service(driver_path)

# Function to initialize WebDriver
def init_driver():
    return webdriver.Firefox(service=service)

# Function to extract product details from a page
def extract_product_details(soup, base_url, driver, wait):
    products = []
    try:
        product_cards = soup.find_all('div', class_='productCardRevamped_container__aJ6lA')

        if not product_cards:
            logging.error("No product cards found. Please check the class name or HTML structure.")
            return products

        for product in product_cards:
            try:
                name_tag = product.find('div', class_='productCardRevamped_productName__aEF8u')
                price_tag = product.find('div', class_='productCardRevamped_price__cWkdn')
                mrp_tag = product.find('span', class_='productCardRevamped_mrpPrice__Yz_Yd')
                discount_tag = product.find('div', class_='productCardRevamped_discount__GSjgY')
                link_tag = product.find_parent('a', href=True)
                brand_tag = product.find('div', class_='productCardRevamped_brandContainer__1mgym')

                if name_tag and price_tag and link_tag and brand_tag:
                    name = name_tag.text.strip()
                    price = price_tag.text.strip()
                    mrp = mrp_tag.text.strip() if mrp_tag else "N/A"
                    discount = discount_tag.text.strip().replace(" Off", "") if discount_tag else "N/A"
                    brand = brand_tag.text.strip()
                    link = link_tag['href']

                    if not link.startswith('https://'):
                        full_link = urljoin(base_url, link)
                    else:
                        full_link = link

                    # Navigate to the product page
                    driver.get(full_link)
                    logging.info(f"Fetching product page: {full_link}")

                    # Wait for the specifications to load
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pdp_specsKey__5LWXC')))

                    # Parse the product page with BeautifulSoup
                    product_soup = BeautifulSoup(driver.page_source, 'html.parser')

                    # Find all specification keys and values
                    spec_keys = product_soup.find_all('div', class_='pdp_specsKey__5LWXC')
                    spec_values = product_soup.find_all('div', class_='pdp_specsValue__fDPie')

                    # Create a dictionary to store specifications
                    specifications = {}
                    for key, value in zip(spec_keys, spec_values):
                        key_text = key.find('p').text.strip()
                        value_text = value.find('p').text.strip()
                        specifications[key_text] = value_text

                    # Extract SKU code from the URL
                    sku_code = full_link.split('/')[-1]

                    # Extract breadcrumbs
                    breadcrumbs = []
                    breadcrumb_container = product_soup.find('div', class_='breadcrumbs_customContainer__SwqCF')
                    if breadcrumb_container:
                        breadcrumb_items = breadcrumb_container.find_all('li', class_='breadcrumbs_breadcrumbItem__TEokw')
                        for item in breadcrumb_items:
                            breadcrumb_text = item.get_text(strip=True)
                            if breadcrumb_text.lower() != "home":
                                breadcrumbs.append(breadcrumb_text)

                    # Create categories based on breadcrumb path
                    categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
                    breadcrumb_categories = {}
                    for i, category in enumerate(categories):
                        if i < len(breadcrumbs):
                            breadcrumb_categories[category] = breadcrumbs[i]
                        else:
                            breadcrumb_categories[category] = ''

                    # Combine product details with specifications and breadcrumb categories
                    product_details = {
                        'Name': name,
                        'Price': price,
                        'Mrp': mrp,
                        'Discount': discount,
                        'Brand': brand,
                        'Link': full_link,
                        'SKU_code': sku_code,
                        'Path': ' > '.join(breadcrumbs)
                    }
                    product_details.update(breadcrumb_categories)
                    product_details.update(specifications)

                    products.append(product_details)
                else:
                    logging.error("Product title, price tag, link, or brand not found. Please check the class names.")
            except Exception as e:
                logging.error(f"Error processing product: {e}")
    except Exception as e:
        logging.error(f"Error extracting product details: {e}")
    
    return products

# URL of the site to scrape
base_url = "https://www.hippostores.com/k-/productlist?sort=relevance"
products = []

# Initialize WebDriver
driver = init_driver()

# Create the WebDriverWait instance after the driver is initialized
wait = WebDriverWait(driver, 10)

# Directory to save the batches
batch_dir = 'batches'
os.makedirs(batch_dir, exist_ok=True)

# Periodic saving interval
save_interval = 50
batch_number = 0

try:
    # Iterate through pages in batches
    for batch_start in range(1, 309, save_interval):
        batch_end = min(batch_start + save_interval, 309)
        logging.info(f"Processing batch from page {batch_start} to {batch_end}")
        for page in range(batch_start, batch_end):
            try:
                url = f"{base_url}&page={page}"
                logging.info(f"Fetching URL: {url}")
                driver.get(url)

                # Wait for the product cards to load
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'productCardRevamped_container__aJ6lA')))

                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Extract product details
                products.extend(extract_product_details(soup, base_url, driver, wait))
                logging.info(f"Page {page} processed successfully")
            except Exception as e:
                logging.error(f"Error processing page {page}: {e}")

        # Save the batch
        batch_file = os.path.join(batch_dir, f'batch_{batch_number}.pkl')
        pd.DataFrame(products).to_pickle(batch_file)
        logging.info(f"Saved batch {batch_number} to {batch_file}")
        batch_number += 1
        products = []  # Reset products list

        # Close and restart the WebDriver to free memory
        driver.quit()
        driver = init_driver()
        wait = WebDriverWait(driver, 10)  # Reinitialize the WebDriverWait
        logging.info("WebDriver restarted")

        # Force garbage collection
        gc.collect()
        logging.info("Garbage collection executed")

finally:
    # Ensure the driver is closed
    driver.quit()
    logging.info("Finalized and closed WebDriver")

# Load all batches and concatenate them into a single DataFrame
all_products = []
for batch_file in sorted(os.listdir(batch_dir)):
    if batch_file.endswith('.pkl'):
        batch_path = os.path.join(batch_dir, batch_file)
        batch_df = pd.read_pickle(batch_path)
        all_products.append(batch_df)
df = pd.concat(all_products, ignore_index=True)

# Number of items downloaded
num_items_downloaded = len(df)
print(f"Number of items downloaded: {num_items_downloaded}")

# Check if 'Category 1' exists in the DataFrame
if 'Category 1' not in df.columns:
    logging.error("'Category 1' column is missing from the DataFrame.")
else:
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter('Final_hippo_scraper.xlsx', engine='xlsxwriter')

    try:
        # Group by 'Category 1' and write each group to a separate sheet
        sheet_names = {}
        for category, group in df.groupby('Category 1'):
            base_sheet_name = (category[:28] + '...') if category and len(category) > 31 else (category if category else 'Uncategorized')
            sheet_name = base_sheet_name
            count = 1
            while sheet_name in sheet_names:
                sheet_name = f"{base_sheet_name}_{count}"
                count += 1
            sheet_names[sheet_name] = True

            group.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Save the DataFrame with the grouped sheets to an Excel file
        writer.close()
        logging.info("Final Excel file saved as 'Final_scraper.xlsx'")
    except Exception as e:
        logging.error(f"Error writing to Excel: {e}")

print("Final_hippo_scraper.xlsx")
