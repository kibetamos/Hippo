from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import pandas as pd

def scroll_to_bottom(driver):
    """Scrolls to the bottom of the page to load all products."""
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_product_details(driver):
    """Extracts details of all products on the page."""
    products = []

    # Find all product elements on the page
    product_elements = driver.find_elements(By.CSS_SELECTOR, '.product-card-selector')  # Replace with actual product selector
    for product_element in product_elements:
        product_url = product_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(product_url)
        time.sleep(5)

        specs, description, price_per_piece, mrp, discount, tax = get_specifications_and_description(driver)
        products.append({
            'URL': product_url,
            'Specifications': specs,
            'Description': description,
            'Price per Piece': price_per_piece,
            'MRP': mrp,
            'Discount': discount,
            'Tax': tax
        })

    return products

def get_specifications_and_description(driver):
    """Extracts specifications and descriptions from the product detail page."""
    specs = {}
    description = {}
    price_per_piece, mrp, discount, tax = None, None, None, None

    # Extract specifications
    try:
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

    # Extract description
    try:
        description_div = driver.find_element(By.CSS_SELECTOR, '#description')
        description_elements = description_div.find_elements(By.XPATH, './/*')
        current_heading = None
        content = []

        for elem in description_elements:
            tag_name = elem.tag_name
            text = elem.text.strip()

            if tag_name == 'h2':
                if current_heading:
                    description[current_heading] = '\n'.join(content).strip()
                current_heading = text
                content = []
                description[current_heading] = ''
            elif tag_name == 'p' or tag_name == 'li':
                content.append(text)
            elif tag_name == 'ul':
                items = [f'• {li.text.strip()}' for li in elem.find_elements(By.TAG_NAME, 'li')]
                content.append('\n'.join(items))
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

        if current_heading:
            description[current_heading] = '\n'.join(content).strip()

    except Exception as e:
        logging.error(f"Error extracting description: {e}")

    # Extract prices and other details
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

def save_to_excel(products, file_name='products.xlsx'):
    """Saves the extracted product details to an Excel file."""
    df = pd.DataFrame(products)
    df.to_excel(file_name, index=False)

if __name__ == "__main__":
    driver = webdriver.Firefox()

    url = "https://mccoymart.com/buy/aac-blocks/"  # Replace with the actual URL
    driver.get(url)
    scroll_to_bottom(driver)
    
    products = extract_product_details(driver)
    save_to_excel(products)

    driver.quit()
