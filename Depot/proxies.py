import requests
from bs4 import BeautifulSoup

# URL of the proxy list
url = "https://spys.one/free-proxy-list/IN/"

# Send a GET request to the website
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Check if the request was successful
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table or other relevant HTML elements containing proxy data
    table = soup.find('table')  # Adjust this selector based on actual HTML structure
    
    # Extract proxies from the table (this will need to be customized based on the actual HTML)
    for row in table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        ip = columns[0].text  # Extract IP address
        port = columns[1].text  # Extract port number
        print(f"IP: {ip}, Port: {port}")
    
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
