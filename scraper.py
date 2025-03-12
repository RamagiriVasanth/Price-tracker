import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send GET request to the URL
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve the page. Status code: {response.status_code}")

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Print the page HTML for debugging purposes
    print(soup.prettify())  # Comment out this line after debugging

    # Try to find the price tag
    price_tag = soup.find('span', {'class': 'a-price-whole'})  # Check if this matches your target page
    if price_tag:
        price = price_tag.text.strip().replace(',', '')  # Clean up the price string
        return float(price)  # Return the price as a float
    else:
        raise ValueError("Could not find the price on the page")
