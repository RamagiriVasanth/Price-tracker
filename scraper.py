import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape price from an Amazon page (adjust based on your target page structure)
    # You might need to adjust this based on the website you're scraping from.
    price_tag = soup.find('span', {'class': 'a-price-whole'})  # Modify based on the actual page structure
    if price_tag:
        price = price_tag.text.strip().replace(',', '')  # Clean up the price string
        return float(price[1:])  # Remove ₹ symbol and convert to float
    else:
        raise ValueError("Could not find the price on the page")
