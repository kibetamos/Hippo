import asyncio
import nodriver as uc

async def main():
    browser = None
    page = None

    try:
        # Launch the browser and open the Upwork job search page
        browser = await uc.start()
        page = await browser.get("https://www.upwork.com/nx/search/jobs/?location=Americas&q=google%20ads&sort=recency")
        
        # Save a screenshot of the page
        await page.save_screenshot('upwork_job_search_page.png')
        print('Screenshot taken and saved as "upwork_job_search_page.png".')

        # Get the page content and save it to a file
        content = await page.get_content()
        with open('upwork_job_search_page.html', 'w', encoding='utf-8') as file:
            file.write(content)
        print('Page content saved as "upwork_job_search_page.html".')

        # Scroll down to load more content (if applicable)
        await page.scroll_down(1500)  # Adjust the scroll amount if needed
        print('Scrolled down to load more content.')

        # Wait for 7 seconds to ensure all content is loaded
        await asyncio.sleep(7)
        print('Waited for 7 seconds.')

        # Find elements with src attributes and flash them
        elems = await page.select_all('*[src]')
        for elem in elems:
            await elem.flash()
        print(f'Found and flashed {len(elems)} elements with src attributes.')

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
