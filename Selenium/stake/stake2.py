import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize undetected-chromedriver
options = uc.ChromeOptions()
options.headless = True  # Set to False if you want to see the browser
driver = uc.Chrome(options=options, use_subprocess=False)

# Example function to get leaderboard data
def get_leaderboard(url):
    try:
        # Open the URL
        driver.get(url)

        # Wait for the leaderboard to load and locate the table rows
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr"))
        )

        leaderboard = []
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")
        
        for row in rows[1:]:  # Skipping the header row
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 1:
                rank = cells[0].text
                user = cells[1].text
                wagered = cells[2].text
                prize = cells[3].text
                leaderboard.append({
                    "rank": rank,
                    "user": user,
                    "wagered": wagered,
                    "prize": prize
                })
        return leaderboard
    except Exception as e:
        print(f"Error getting leaderboard data: {str(e)}")
        # Take a screenshot for debugging
        driver.save_screenshot('error_screenshot.png')
        return []
    finally:
        driver.quit()

# URL of the page to scrape
url = 'https://www.stake.us/challenges'

# Get leaderboard data
leaderboard_data = get_leaderboard(url)

# Print the data
for data in leaderboard_data:
    print(data)
