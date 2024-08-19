import asyncio
import nodriver as uc

async def main():
    browser = None

    try:
        # Launch the browser and open the Upwork login page
        browser = await uc.start()
        page = await browser.get("https://www.upwork.com/ab/account-security/login")

        # Wait for the page to load by checking for a specific element
        # You might need to adjust this based on your page structure
        # await page.wait_for_selector('#login_username', timeout=10000)  # Wait for the username field to be visible
        
        # Optionally save a screenshot
        await page.save_screenshot()
        print("Screenshot taken and saved as 'upwork_login_page.png'.")

        # Optionally get the page content
        content = await page.get_content()

        print("Page content retrieved.")

        # Optionally save the page content to a file
        with open('upwork_login_page.html', 'w', encoding='utf-8') as file:
            file.write(content)
        print("Page content saved as 'upwork_login_page.html'.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        if browser:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
