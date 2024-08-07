import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time

# Setup logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Firefox options
firefox_options = Options()
# firefox_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize the WebDriver for Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

def load_all_products():
    """Scrolls to the bottom of the page to ensure all products are loaded and returns the number of products."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for additional content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info("Reached the end of the page or no more content to load.")
                break
            last_height = new_height
        except Exception as e:
            logging.error(f"Error during scrolling: {e}")
            break

    # Count the number of product elements, filtering out duplicates
    try:
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')
        product_links = set()
        for product in product_elements:
            link = product.get_attribute('href')
            if link:
                product_links.add(link)
        product_count = len(product_links)
        logging.info(f"Total number of unique products found: {product_count}")
    except Exception as e:
        logging.error(f"Error counting products: {e}")
        product_count = 0

    return product_count



def scroll_until_description_in_view(description_selector):
    """Scrolls until the product description section is in view."""
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, description_selector)))
            break
        except Exception as e:
            logging.error(f"Error checking description visibility: {e}")

def get_specifications_and_description(url):
    """Extracts specifications and descriptions from the product detail page."""
    driver.get(url)
    time.sleep(10)

    specs = {}
    description = {
        'Product Description': '',
        'Key Features': '',
        'Benefit & Advantages': '',
        'Surface Preparation': '',
        'Applications': ''
    }
    price_per_piece, mrp, discount, tax = None, None, None, None

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table-Specifications')))
        spec_elements = driver.find_elements(By.CSS_SELECTOR, '.table-Specifications tr')
        for spec in spec_elements:
            key_element = spec.find_element(By.CSS_SELECTOR, 'td b')
            key = key_element.text.strip() if key_element else None
            value_elements = spec.find_elements(By.CSS_SELECTOR, 'td')
            value = value_elements[1].text if len(value_elements) > 1 else ''
            if key:
                specs[key] = value
    except Exception as e:
        logging.error(f"Error extracting specifications for product {url}: {e}")

    try:
        description_div = driver.find_element(By.CSS_SELECTOR, '#description')
        description_elements = description_div.find_elements(By.XPATH, './/*')
        current_heading = None
        content = []

        for elem in description_elements:
            if elem.tag_name == 'h2':
                if current_heading:
                    description[current_heading] = '\n'.join(content).strip()
                current_heading = elem.text.strip()
                content = []
                if current_heading not in description:
                    description[current_heading] = ''
            elif elem.tag_name == 'p':
                content.append(elem.text.strip())
            elif elem.tag_name == 'ul':
                items = [li.text.strip() for li in elem.find_elements(By.TAG_NAME, 'li')]
                content.append('\n'.join(items))

        if current_heading:
            description[current_heading] = '\n'.join(content).strip()
    except Exception as e:
        logging.error(f"Error extracting description for product {url}: {e}")

    try:
        price_per_piece_element = driver.find_element(By.CSS_SELECTOR, '.price-pcs-pdp')
        price_per_piece = price_per_piece_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting price per piece for product {url}: {e}")

    try:
        mrp_element = driver.find_element(By.CSS_SELECTOR, '.discount-price-pdp strike')
        mrp = mrp_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting MRP for product {url}: {e}")

    try:
        discount_element = driver.find_element(By.CSS_SELECTOR, '.off-price-pdp')
        discount = discount_element.text.strip().replace('off', '').strip()
    except Exception as e:
        logging.error(f"Error extracting discount for product {url}: {e}")

    try:
        tax_element = driver.find_element(By.CSS_SELECTOR, '.included-texes-pdp')
        tax = tax_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting tax for product {url}: {e}")

    return specs, description, price_per_piece, mrp, discount, tax

def get_breadcrumb_path():
    """Extracts the breadcrumb path and splits it into categories."""
    try:
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, 'ol.d-flex li')
        path_list = [element.text.strip() for element in breadcrumb_elements if element.text.strip()]
        path_list_reduced = path_list[2:-1]  # Remove the first two and last elements
    except Exception as e:
        logging.error(f"Error extracting breadcrumb path: {e}")
        path_list_reduced = []

    path_dict = {f'Category {i+1}': path_list_reduced[i] for i in range(len(path_list_reduced))}
    full_path = ' > '.join(path_list_reduced)
    path_dict['Path'] = full_path

    return path_dict

# Main scraping process
driver.get('https://mccoymart.com/buy/block-board/')
load_all_products()

product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')
product_links = [product.get_attribute('href') for product in product_elements]
unique_links = set(product_links)

products = []

for i, link in enumerate(list(unique_links)[:2]):
    driver.get(link)
    time.sleep(10)
    scroll_until_description_in_view('#description')

    product_info = {'Link': link, 'Status': 'Failed'}

    try:
        title = driver.find_element(By.CSS_SELECTOR, '.products-content-details').text.strip()
        product_info['Title'] = title
    except Exception as e:
        logging.error(f"Error extracting title for product {link}: {e}")

    try:
        pack_price_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityAmount')
        pack_price = pack_price_element.text.strip()
        product_info['Pack Price'] = pack_price
    except Exception as e:
        logging.error(f"Error extracting pack price for product {link}: {e}")

    try:
        quantity_element = driver.find_element(By.CSS_SELECTOR, '.price-dtls-pay-values .packQuantityPcs')
        quantity = quantity_element.text.strip()
        product_info['Quantity'] = quantity
    except Exception as e:
        logging.error(f"Error extracting quantity for product {link}: {e}")

    try:
        specifications, description, price_per_piece, mrp, discount, tax = get_specifications_and_description(link)
        breadcrumb_path = get_breadcrumb_path()
        product_info.update({
            'MRP': mrp,
            'Pack Price': pack_price,
            'Discount': discount,
            'Tax': tax,
            'Price Per Piece': price_per_piece,
            'Quantity': quantity,
            'Product Description': description.get('Product Description', ''),
            'Status': 'Success'
        })
        product_info.update(specifications)
        product_info.update(breadcrumb_path)
    except Exception as e:
        logging.error(f"Error extracting product details for product {link}: {e}")

    products.append(product_info)

driver.quit()

df = pd.DataFrame(products)

# Group by 'Category 1' and save to Excel
try:
    with pd.ExcelWriter('sample5.xlsx', engine='openpyxl') as writer:
        for category, group in df.groupby('Category 1'):
            safe_category = str(category).replace('/', '_').replace('\\', '_')
            group.to_excel(writer, sheet_name=safe_category, index=False)
except Exception as e:
    logging.error(f"Error saving to Excel: {e}")
