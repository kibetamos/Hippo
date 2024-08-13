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
    """Scrolls to the bottom of the page to ensure all products are loaded and returns the product URLs."""
    product_links = set()
    try:
        # Wait until the page has loaded some key elements indicating that content is fully loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards'))
        )
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(20)  # Wait for additional content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info("Reached the end of the page or no more content to load.")
                break
            last_height = new_height
        
        # After scrolling to the bottom, ensure all products are loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a'))
        )
        
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.item.global-card-list.brands-mccoy-cards a')
        for product in product_elements:
            link = product.get_attribute('href')
            if link:
                product_links.add(link)
        
        logging.info(f"Total number of unique products found: {len(product_links)}")
    except Exception as e:
        logging.error(f"Error during product loading and counting: {e}")

    return list(product_links)

def scroll_until_description_in_view(description_selector):
    """Scrolls until the product description section is in view."""
    max_attempts = 3
    for _ in range(max_attempts):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, description_selector)))
            break
        except Exception as e:
            logging.error(f"Error checking description visibility: {e}")

def get_specifications_and_description():
    """Extracts specifications and descriptions from the product detail page."""
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
        logging.error(f"Error extracting specifications: {e}")
    try:
        description_div = driver.find_element(By.CSS_SELECTOR, '#description')
        description_elements = description_div.find_elements(By.XPATH, './/*')
        current_heading = None
        content = []
        description = {}

        for elem in description_elements:
            tag_name = elem.tag_name
            text = elem.text.strip()

            if tag_name == 'h2':
                # Save the content under the previous heading if it exists
                if current_heading:
                    description[current_heading] = '\n'.join(content).strip()
                # Update to the new heading
                current_heading = text
                content = []  # Reset content for the new heading
                description[current_heading] = ''  # Initialize the new heading in the dictionary
            elif tag_name == 'p':
                content.append(text)
            elif tag_name == 'ul':
                items = [f'• {li.text.strip()}' for li in elem.find_elements(By.TAG_NAME, 'li')]
                content.append('\n'.join(items))
            elif tag_name == 'li':
                # Directly handle li tags to ensure they're captured correctly
                content.append(f'• {text}')
            elif tag_name == 'span':
                content.append(text)
            elif tag_name == 'div':
                if text:
                    content.append(text)
            elif tag_name == 'img':
                img_src = elem.get_attribute('src')
                if img_src:
                    content.append(f'Image URL: {img_src}')
            elif tag_name == 'a':
                link_href = elem.get_attribute('href')
                if link_href:
                    content.append(f'Link: {text} ({link_href})')

        # Save the content under the last heading
        if current_heading:
            description[current_heading] = '\n'.join(content).strip()

    except Exception as e:
        print(f"An error occurred: {e}")

    # try:
    #     description_div = driver.find_element(By.CSS_SELECTOR, '#description')
    #     description_elements = description_div.find_elements(By.XPATH, './/*')
    #     current_heading = None
    #     content = []

    #     for elem in description_elements:
    #         if elem.tag_name == 'h2' :
    #             if current_heading:
    #                 description[current_heading] = '\n'.join(content).strip()
    #             current_heading = elem.text.strip()
    #             content = []
    #             if current_heading not in description:
    #                 description[current_heading] = ''
    #         elif elem.tag_name == 'p':
    #             content.append(elem.text.strip())
    #         elif elem.tag_name == 'ul':
    #             items = [li.text.strip() for li in elem.find_elements(By.TAG_NAME, 'li')]
    #             content.append('\n'.join(items))

    #     if current_heading:
    #         description[current_heading] = '\n'.join(content).strip()
    # except Exception as e:
    #     logging.error(f"Error extracting description: {e}")

    try:
        price_per_piece_element = driver.find_element(By.CSS_SELECTOR, '.price-pcs-pdp')
        price_per_piece = price_per_piece_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting price per piece: {e}")

    try:
        mrp_element = driver.find_element(By.CSS_SELECTOR, '.discount-price-pdp strike')
        mrp = mrp_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting MRP: {e}")

    try:
        discount_element = driver.find_element(By.CSS_SELECTOR, '.off-price-pdp')
        discount = discount_element.text.strip().replace('off', '').strip()
    except Exception as e:
        logging.error(f"Error extracting discount: {e}")

    try:
        tax_element = driver.find_element(By.CSS_SELECTOR, '.included-texes-pdp')
        tax = tax_element.text.strip()
    except Exception as e:
        logging.error(f"Error extracting tax: {e}")

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
    path_dict['Path'] = ' > '.join(path_list_reduced)

    return path_dict

# List of URLs to scrape
urls = [
    'https://mccoymart.com/buy/shuttering-plywood/',
]

products = []
visited_links = set()

for url in urls:
    try:
        driver.get(url)
        product_links = load_all_products()  # Now returns a list of product URLs
        
        for link in product_links:
            if link not in visited_links:
                visited_links.add(link)
                driver.get(link)
                time.sleep(15)
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
                    specifications, description, price_per_piece, mrp, discount, tax = get_specifications_and_description()
                    breadcrumb_path = get_breadcrumb_path()
                    product_info.update({
                        'MRP': mrp,
                        'Discount': discount,
                        'Tax': tax,
                        'Price Per Piece': price_per_piece,
                        'Product Description': description.get('Product Description', ''),
                        'Status': 'Success'
                    })
                    product_info.update(specifications)
                    product_info.update(breadcrumb_path)
                except Exception as e:
                    logging.error(f"Error extracting product details for product {link}: {e}")

                products.append(product_info)

    except Exception as e:
        logging.error(f"Error processing URL {url}: {e}")

# Save products to Excel
driver.quit()
df = pd.DataFrame(products)

# Group by 'Category 1' and save to Excel
try:
    with pd.ExcelWriter('sa.xlsx') as writer:
        for category, group_df in df.groupby('Category 1'):
            group_df.to_excel(writer, sheet_name=category[:30], index=False)
        logging.info("Data saved successfully to 'sa.xlsx'")
except Exception as e:
    logging.error(f"Error saving data to Excel: {e}")
