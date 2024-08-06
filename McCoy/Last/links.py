from bs4 import BeautifulSoup

def extract_names_and_urls(html_file_path):
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Initialize an empty list to store the extracted data
    data = []

    # Find all navigation items
    nav_items = soup.select('nav.botton-nav-wrapper ul li')

    for item in nav_items:
        # Find the link within each navigation item
        link = item.find('a', href=True)
        if link:
            name = link.get_text(strip=True)
            url = link['href']
            if name and url:
                data.append({'name': name, 'url': url})

    return data

def save_to_file(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"Name: {item['name']}, URL: {item['url']}\n")

def main():
    # Path to your HTML file
    html_file_path = '/home/amos/Documents/projects/Hippo/McCoy/Last/index.html'
    
    # Path to save the output
    output_file_path = 'extracted_data.txt'

    # Extract names and URLs
    results = extract_names_and_urls(html_file_path)

    # Print results to console
    for item in results:
        print(f"Name: {item['name']}, URL: {item['url']}")

    # Save results to a file
    save_to_file(results, output_file_path)

if __name__ == '__main__':
    main()
