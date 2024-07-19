from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import xlsxwriter

# Path to GeckoDriver
driver_path = '/usr/bin/geckodriver'
service = Service(driver_path)

# Initialize the Firefox WebDriver
driver = webdriver.Firefox(service=service)

# Function to extract product details from a page
def extract_product_details(soup):
    products = []

    product_cards = soup.find_all('div', class_='productCardRevamped_container__aJ6lA')

    if not product_cards:
        print("No product cards found. Please check the class name or HTML structure.")
        return products

    for product in product_cards:
        name_tag = product.find('div', class_='productCardRevamped_productName__aEF8u')
        price_tag = product.find('div', class_='productCardRevamped_price__cWkdn')
        mrp_tag = product.find('span', class_='productCardRevamped_mrpPrice__Yz_Yd')
        discount_tag = product.find('div', class_='productCardRevamped_discount__GSjgY')
        link_tag = product.find_parent('a', href=True)  # Assuming the link is in a parent 'a' tag
        brand_tag = product.find('div', class_='productCardRevamped_brandContainer__1mgym')  # Brand tag

        if name_tag and price_tag and link_tag and brand_tag:
            name = name_tag.text.strip()
            price = price_tag.text.strip()
            mrp = mrp_tag.text.strip() if mrp_tag else "N/A"
            discount = discount_tag.text.strip().replace(" off", "") if discount_tag else "N/A"  # Remove " off" from discount
            brand = brand_tag.text.strip()  # Extract brand
            link = link_tag['href']

            # Check if the link has a scheme, if not prepend the base URL
            if not link.startswith('https://'):
                full_link = urljoin(base_url, link)
            else:
                full_link = link

            # Navigate to the product page
            driver.get(full_link)

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
                    if breadcrumb_text.lower() != "home":  # Exclude "home" from breadcrumbs
                        breadcrumbs.append(breadcrumb_text)

            # Create categories based on breadcrumb path
            categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']  # Adjust as needed
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
            print("Product title, price tag, link, or brand not found. Please check the class names.")
    
    return products

# URL of the site to scrape
base_url = "https://www.hippostores.com/k-/productlist?sort=relevance"
products = []
wait = WebDriverWait(driver, 10)

# Iterate through 4 pages
for page in range(1, 5):
    url = f"{base_url}&page={page}"
    driver.get(url)

    # Wait for the product cards to load
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'productCardRevamped_container__aJ6lA')))

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract product details
    products.extend(extract_product_details(soup))

# Close the driver
driver.quit()

# Number of items downloaded
num_items_downloaded = len(products)
print(f"Number of items downloaded: {num_items_downloaded}")

# Create a DataFrame from the product details
df = pd.DataFrame(products)

# Create a Pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter('products_by_category.xlsx', engine='xlsxwriter')

# Group by 'Category 1' and write each group to a separate sheet
for category, group in df.groupby('Category 1'):
    sheet_name = category if category else 'Uncategorized'
    group.to_excel(writer, sheet_name=sheet_name, index=False)

# Save the DataFrame with the grouped sheets to an Excel file
writer.save()

print("Product details saved to products_by_category.xlsx")
