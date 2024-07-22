import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.stake.us/challenges"

# Send a GET request to the URL
response = requests.get(url)

# Parse the page content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table by its class
table = soup.find('table', {'class': 'table-content'})

# Initialize a list to hold the extracted data
top_wins = []

# Iterate through each row in the table
for row in table.find_all('tr', {'data-bet-index': True}):
    columns = row.find_all('td')
    
    # Extract game name
    game_name = columns[0].text.strip()
    
    # Extract user
    user = columns[1].text.strip()
    
    # Extract time
    time = columns[2].text.strip()
    
    # Extract bet amount
    bet_amount = columns[3].text.strip()
    
    # Extract multiplier
    multiplier = columns[4].text.strip()
    
    # Extract payout
    payout = columns[5].text.strip()
    
    # Append the extracted data as a dictionary
    top_wins.append({
        'game_name': game_name,
        'user': user,
        'time': time,
        'bet_amount': bet_amount,
        'multiplier': multiplier,
        'payout': payout
    })

# Print the extracted data
for win in top_wins:
    print(win)
