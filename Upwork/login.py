def load_cookies(driver, cookies_file):
    """Load cookies from a JSON file into the WebDriver session."""
    try:
        with open(cookies_file, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                # Convert expirationDate from timestamp to int if present
                if 'expirationDate' in cookie:
                    cookie['expiry'] = int(cookie['expirationDate'])
                # Ensure the domain is correct
                if 'domain' not in cookie:
                    cookie['domain'] = '.upwork.com'
                driver.add_cookie(cookie)
    except Exception as e:
        print(f'Error loading cookies: {e}')
