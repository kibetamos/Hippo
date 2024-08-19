import asyncio
import nodriver as uc

async def main():
    browser = None

    try:
        # Launch the browser and open the Upwork login page
        browser = await uc.start()
        page = await browser.get("https://www.upwork.com/ab/account-security/login")

        # Log in to Upwork
        await page.type('input[name="login[username]"]', 'arunk.gopalakrishnan@gmail.com')
        await page.type('input[name="login[password]"]', 'LAVisionPro!')
        await page.click('button[type="submit"]')

        # Wait for the page to load after login
        await asyncio.sleep(5)

        # Navigate to the job search page
        await page.goto("https://www.upwork.com/search/jobs/")

        # Optionally, perform a search by typing a keyword and clicking the search button
        await page.type('input[data-test="search-input"]', 'data science')
        await page.click('button[data-test="search-button"]')
        
        # Wait for the results to load
        await asyncio.sleep(10)

        # Find all the job title links
        job_title_selector = 'h4.job-title a'
        job_title_elements = await page.select_all(job_title_selector)
        
        # Output the number of job titles found and optionally print them
        print(f'Number of job titles found: {len(job_title_elements)}')
        for element in job_title_elements:
            title_text = await element.text()
            print(f'Job Title: {title_text}')
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        if browser:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
