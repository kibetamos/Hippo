from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

# Path to the geckodriver executable
GECKODRIVER_PATH = '/usr/bin/geckodriver'  # Update this path

def main():
    # Set up Firefox options
    options = Options()
    options.headless = False  # Set to True if you want to run in headless mode

    # Initialize the WebDriver
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Open the Upwork job search page
        # driver.get("https://www.upwork.com/nx/search/jobs/?hourly_rate=50-&nbs=1&payment_verified=1&q=google%20ads&sort=recency&t=0&user_location_match=1&page=1&per_page=50")

        driver.get("https://www.upwork.com/nx/search/jobs/?location=Americas&q=google%20ads&sort=recency")

        # Wait for the page to fully load
        time.sleep(5)
        print('Waited for 5 seconds to ensure the page is fully loaded.')

        # Scroll down to load more content (adjust as needed)
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(3):  # Adjust the range for more scrolling
            body.send_keys(Keys.END)
            time.sleep(5)  # Wait to ensure content is fully loaded

        # Find all job listing elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'article[data-test="JobTile"] a.up-n-link')

        if not job_elements:
            print('No job listings found.')
            return

        print(f'Found {len(job_elements)} job listings.')

        # Extract and print job titles and URLs
        for job in job_elements:
            try:
                # Safely get the text content and URL
                title = job.text
                url = job.get_attribute('href')

                # Ensure the URL is absolute
                if url and not url.startswith('http'):
                    url = 'https://www.upwork.com' + url

                # Check if title and URL are not None
                if title and url:
                    print(f'Job Title: {title.strip()}')
                    print(f'Job URL: {url}')
                    print('---')
                else:
                    print('Incomplete job listing details.')

            except Exception as e:
                print(f'Error extracting details from a job listing: {e}')

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        # Close the browser
        driver.quit()
        print('Browser closed.')

if __name__ == '__main__':
    main()




