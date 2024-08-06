import asyncio
import nodriver as uc

async def main():
    # Initialize the browser
    browser = await uc.start()
    page = await browser.get('https://mccoymart.com/buy/')

    # Wait for the page to fully load
    await asyncio.sleep(5)  # Adjust sleep time if needed

    # Find the "Shop" link using a more general selector
    shop_link = await page.query('div.heading-new a[href="/buy/"]')
    if shop_link:
        # Hover over the "Shop" link
        await shop_link.hover()

        # Wait for the subcategory menu to appear
        await asyncio.sleep(2)  # Adjust sleep time if needed

        # Extract the subcategory links
        subcategory_elements = await page.query_all('div.heading-new a[href="/buy/"] + div a')
        subcategory_links = [await elem.get_attribute('href') for elem in subcategory_elements if await elem.get_attribute('href')]

        # Print the extracted links
        for link in subcategory_links:
            print(link)
    
    # Close the browser
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
