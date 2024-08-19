import asyncio
import nodriver as uc

async def main():
    browser = None
    page = None

    try:
        # Launch the browser and open the Upwork job search page
        browser = await uc.start()
        page = await browser.get("https://www.upwork.com/nx/search/jobs/?location=Americas&q=google%20ads&sort=recency")

        # Wait for 5 seconds to ensure the page is fully loaded
        await asyncio.sleep(5)
        print('Waited for 5 seconds to ensure the page is fully loaded.')

        # Scroll down to load more content (if applicable)
        await page.scroll_down(15)  # Adjust the scroll amount if needed
        print('Scrolled down to load more content.')

        # Wait for an additional 5 seconds to ensure all content is fully loaded after scrolling
        await asyncio.sleep(5)
        print('Waited for 5 seconds after scrolling to ensure content is fully loaded.')

        # Find all job listing elements
        job_elements = await page.select_all('article[data-test="JobTile"] a.up-n-link')

        if not job_elements:
            print('No job listings found.')
            return

        print(f'Found {len(job_elements)} job listings.')

        # Extract and print job titles and URLs
        for job in job_elements:
            try:
                # Safely get the text content and URL
                title = await job.get_attribute('textContent')
                url = await job.get_attribute('href')
                
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
        # Close the page if it is open
        if page:
            await page.close()
            print('Page closed.')

if __name__ == '__main__':
    # Run the main function using the event loop
    uc.loop().run_until_complete(main())
