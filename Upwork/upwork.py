from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Path to the geckodriver executable
GECKODRIVER_PATH = '/usr/bin/geckodriver'  # Update this path

def save_to_file(job_listings):
    with open('vedio_ed.txt', 'w') as file:
        file.write(f'Number of job listings found: {len(job_listings)}\n\n')
        for title, url, date in job_listings:
            file.write(f'Job Title: {title.strip()}\n')
            file.write(f'Job URL: {url}\n')
            file.write(f'Posted: {date}\n')  # Include the posting date
            file.write('---\n')

def main():
    # Set up Firefox options
    options = Options()
    options.headless = False  # Set to True if you want to run in headless mode
    # Initialize the WebDriver
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Open the Upwork job search page
        driver.get("https://www.upwork.com/nx/search/jobs/?hourly_rate=40-&nbs=1&payment_verified=1&per_page=50&q=video%20editing&sort=recency&t=0&user_location_match=1&page=1")
        # driver.get("https://www.upwork.com/nx/search/jobs/?location=Americas&q=google%20ads&sort=recency")
        # Wait for the page to fully load
        time.sleep(5)
        print('Waited for 5 seconds to ensure the page is fully loaded.')


        # Scroll down to load more content (adjust as needed)
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(3):  # Adjust the range for more scrolling
            body.send_keys(Keys.END)
            time.sleep(5)  # Wait to ensure content is fully loaded

        # Find all job listing elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'article[data-test="JobTile"]')

        if not job_elements:
            print('No job listings found.')
            save_to_file([])
            return

        print(f'Found {len(job_elements)} job listings.')

        # Extract job titles, URLs, and posting dates
        job_listings = []
        for job_element in job_elements:
            try:
                # Safely get the title, URL, and posting date
                job_link = job_element.find_element(By.CSS_SELECTOR, 'a.up-n-link')
                title = job_link.text
                url = job_link.get_attribute('href')
                
                # Extract the posted date
                posted_date = job_element.find_element(By.CSS_SELECTOR, 'small[data-test="job-pubilshed-date"]').text

                # Ensure the URL is absolute
                if url and not url.startswith('http'):
                    url = 'https://www.upwork.com' + url

                # Check if title, URL, and date are not None
                if title and url and posted_date:
                    job_listings.append((title, url, posted_date))
                else:
                    print('Incomplete job listing details.')

            except Exception as e:
                print(f'Error extracting details from a job listing: {e}')

        # Save the job listings to a file
        save_to_file(job_listings)

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        # Close the browser
        driver.quit()
        print('Browser closed.')

if __name__ == '__main__':
    main()
