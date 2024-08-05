import asyncio
import nodriver as uc

async def main():
    # Start the browser
    browser = await uc.start()
    
    # Open the specified URL
    page = await browser.get('https://mccoymart.com/buy/aac-blocks/')
    
    # Function to scroll down slowly
    async def slow_scroll(scroll_step=100, wait_time=2):
        previous_height = await page.evaluate('document.body.scrollHeight')
        while True:
            # Scroll down by a small step
            await page.evaluate(f'window.scrollBy(0, {scroll_step})')
            
            # Wait for new content to load
            await asyncio.sleep(wait_time)
            
            # Get new scroll height
            new_height = await page.evaluate('document.body.scrollHeight')
            
            # Break if we've reached the bottom of the page
            if new_height == previous_height:
                break
            previous_height = new_height
    
    # Perform the slow scroll
    await slow_scroll(scroll_step=100, wait_time=12)
    
    # Wait for an additional 10 seconds to ensure all content is loaded
    await asyncio.sleep(10)
    
    # Extract product items
    # items = await page.query_selector_all('.item')  # Adjust the selector as needed
    # print(f"Number of items found: {len(items)}")
    
    # Optionally, you can print details of the items or save screenshots
    # For example:
    # for item in items:
    #     url = await item.evaluate('element => element.querySelector("a") ? element.querySelector("a").href : ""')
    #     print(f"Item URL: {url}")
    
    # Close the browser
    await browser.close()

if __name__ == '__main__':
    # Run the main function using the event loop
    uc.loop().run_until_complete(main())
