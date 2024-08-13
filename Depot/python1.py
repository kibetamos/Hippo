import requests
from bs4 import BeautifulSoup

# URL to inspect
url = "http://www.materialdepot.in/"

# Define the proxy
proxies = {
    'http': 'http://59.89.148.104:8080',
    'https': 'http://59.89.148.104:8080'
}

# Send a GET request to the website using the proxy
try:
    response = requests.get(url, proxies=proxies, timeout=10)
    response.raise_for_status()  # Check if the request was successful
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Pretty print the HTML structure
    print(soup.prettify())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
