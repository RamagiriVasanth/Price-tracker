import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Scrape price from an Amazon page (adjust based on your target page structure)
    price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()
    price = float(price[1:])  # Remove '$' and convert to float
    return price
