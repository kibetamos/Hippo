import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.kaiandkaro.com/vehicles?price__lte=500000"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the vehicle containers
    vehicle_containers = soup.find_all('div', class_='chakra-linkbox')

    # Loop through each vehicle container and extract details
    for vehicle in vehicle_containers:
        # Extract vehicle name
        name = vehicle.find('h2', class_='chakra-heading').text.strip()
        
        # Extract image URL
        img_tag = vehicle.find('img', class_='card-img-top')
        img_url = img_tag['src'] if img_tag else 'No Image'

        # Extract availability status
        availability = vehicle.find('span', class_='chakra-badge css-i1hse3').text.strip()

        # Extract year
        year = vehicle.find('span', class_='chakra-badge css-1dub5x4').text.strip()

        # Extract transmission type, engine capacity, and condition
        specs = vehicle.find_all('span', class_='css-evl6jo')
        transmission = specs[0].text.strip() if len(specs) > 0 else 'N/A'
        engine_capacity = specs[1].text.strip() if len(specs) > 1 else 'N/A'
        condition = specs[2].text.strip() if len(specs) > 2 else 'N/A'

        # Extract description
        description = vehicle.find('p', class_='chakra-text css-1loynb1').text.strip()

        # Extract price
        price_tag = vehicle.find('p', class_='chakra-text css-0')
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Print or store the extracted data
        print(f"Name: {name}")
        print(f"Image URL: {img_url}")
        print(f"Availability: {availability}")
        print(f"Year: {year}")
        print(f"Transmission: {transmission}")
        print(f"Engine Capacity: {engine_capacity}")
        print(f"Condition: {condition}")
        print(f"Description: {description}")
        print(f"Price: {price}")
        print('-' * 40)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
