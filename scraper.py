import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Scrape price from an Amazon page (adjust based on your target page structure)
    price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()  # Amazon's price format

    # Remove '$' and convert to float
    price = price.replace('$', '').strip()  # Remove the dollar symbol
    price = float(price)  # Convert the price to a float

    # Convert the price to INR (Indian Rupees) - assuming a fixed conversion rate
    conversion_rate = 74  # Example conversion rate (USD to INR), you can update it or use a live conversion API
    price_inr = price * conversion_rate  # Convert USD to INR

    return price_inr  # Return the price in INR
