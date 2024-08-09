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

def load_urls_from_file(file_path):
    """Load URLs from a text file."""
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def load_all_products(list_page_url):
    """Extract product links from a product listing page."""
    driver.get(list_page_url)
    scroll_and_load_page()  # Ensure all content is loaded on the listing page

    product_links = set()
    try:
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')
        for product in product_elements:
            link = product.get_attribute('href')
            if link:
                product_links.add(link)
        logging.info(f"Found {len(product_links)} products on page {list_page_url}")
    except Exception as e:
        logging.error(f"Error extracting products from page {list_page_url}: {e}")
    
    return list(product_links)

def scroll_and_load_page():
    """Scrolls down the page to ensure all content is loaded."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Allow time for content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info("Reached the end of the page or no more content to load.")
                break
            last_height = new_height
        except Exception as e:
            logging.error(f"Error during scrolling: {e}")
            break

def scroll_until_description_in_view(description_selector):
    """Scrolls until the product description section is in view."""
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, description_selector)))
            element = driver.find_element(By.CSS_SELECTOR, description_selector)
            if element.is_displayed():
                break
            time.sleep(2)
        except Exception as e:
            logging.error(f"Error checking description visibility: {e}")
            time.sleep(2)

def get_specifications_and_description(url):
    """Extracts specifications and descriptions from the product detail page."""
    driver.get(url)
    time.sleep(10)  # Increased time for page load

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
        # Ensure the page is fully loaded
        scroll_and_load_page()
        
        # Extract specifications
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

        # Extract product description
        try:
            description_div = driver.find_element(By.CSS_SELECTOR, '#description')
            description_elements = description_div.find_elements(By.XPATH, './/*')
            current_heading = None
            content = []

            for elem in description_elements:
                if elem.tag_name in ['h2', 'h3']:
                    if current_heading:
                        description[current_heading] = '\n'.join(content).strip()
                    current_heading = elem.text.strip()
                    content = []
                    if current_heading not in description:
                        description[current_heading] = ''
                elif elem.tag_name == 'p':
                    content.append(elem.text.strip())
                elif elem.tag_name == 'ul':
                    list_items = [li.text.strip() for li in elem.find_elements(By.TAG_NAME, 'li')]
                    content.append('\n'.join(list_items))

            if current_heading:
                description[current_heading] = '\n'.join(content).strip()
        except Exception as e:
            logging.error(f"Error extracting description for product {url}: {e}")

        # Extract price, MRP, discount, and tax
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

    except Exception as e:
        logging.error(f"Error accessing product page for {url}: {e}")

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

def process_product(link):
    """Processes an individual product link and returns its data."""
    product_info = {'Link': link, 'Status': 'Failed'}

    try:
        logging.info(f"Processing product link: {link}")
        driver.get(link)
        scroll_and_load_page()  # Ensure all content is loaded on the product page
        scroll_until_description_in_view('#description')

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
            breadcrumb = get_breadcrumb_path()
            product_info.update(breadcrumb)
        except Exception as e:
            logging.error(f"Error extracting breadcrumb for product {link}: {e}")

        try:
            specs, description, price_per_piece, mrp, discount, tax = get_specifications_and_description(link)
            product_info.update(specs)
            product_info.update(description)
            product_info.update({
                'Price Per Piece': price_per_piece,
                'MRP': mrp,
                'Discount': discount,
                'Tax': tax,
                'Status': 'Success'
            })
        except Exception as e:
            logging.error(f"Error processing product specifications and description for {link}: {e}")

    except Exception as e:
        logging.error(f"Error accessing product page for {link}: {e}")

    return product_info

def save_data_to_excel(data, filename):
    """Saves grouped data to an Excel file."""
    df = pd.DataFrame(data)

    # Assuming 'Category 4' is one of the keys in the data dict
    if 'Category 1' in df.columns:
        df.sort_values(by=['Category 1'], inplace=True)
    
    # Saving to Excel
    df.to_excel(filename, index=False)



def main(input_file, output_file):
    """Main execution function."""
    urls = load_urls_from_file(input_file)
    all_data = []

    for url in urls:
        try:
            product_links = load_all_products(url)
            for link in product_links:
                product_data = process_product(link)
                all_data.append(product_data)
        except Exception as e:
            logging.error(f"Failed to process page {url}: {e}")

    save_data_to_excel(all_data, output_file)

# Main execution
if __name__ == "__main__":
    input_file = 'shops.txt'  # Replace with your input file
    output_file = 'products.xlsx'  # Replace with your output file
    main(input_file, output_file)

    driver.quit()
