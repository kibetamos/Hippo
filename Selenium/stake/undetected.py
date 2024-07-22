import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize undetected-chromedriver
driver = uc.Chrome(headless=True, use_subprocess=False)

# Open the URL
driver.get('https://www.stake.us/')

# Wait for the security check to complete
time.sleep(30)  # Adjust this as needed

# Wait for the specific table to be present in the DOM
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'table-content'))
    )
    print("Table found.")
except Exception as e:
    print(f"Error waiting for the table: {e}")
    driver.quit()
    exit()

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Print the page source for debugging
print(soup.prettify())

# Close the browser
driver.quit()

# Find the table by its class
table = soup.find('table', {'class': 'table-content'})

# Check if the table was found
if table is None:
    print("Error: Table with class 'table-content' not found.")
    exit()

# Initialize a list to hold the extracted data
top_wins = []

# Iterate through each row in the table
for row in table.find_all('tr', {'data-bet-index': True}):
    columns = row.find_all('td')
    
    # Extract game name
    game_name = columns[0].text.strip()
    
    # Extract user
    user = columns[1].text.strip()
    
    # Extract time
    time = columns[2].text.strip()
    
    # Extract bet amount
    bet_amount = columns[3].text.strip()
    
    # Extract multiplier
    multiplier = columns[4].text.strip()
    
    # Extract payout
    payout = columns[5].text.strip()
    
    # Append the extracted data as a dictionary
    top_wins.append({
        'game_name': game_name,
        'user': user,
        'time': time,
        'bet_amount': bet_amount,
        'multiplier': multiplier,
        'payout': payout
    })

# Print the extracted data
for win in top_wins:
    print(win)
