import requests
from bs4 import BeautifulSoup

# Static conversion rate (can be replaced with live data API for accuracy)
USD_TO_INR = 74  # Example conversion rate; change it as needed

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Fetch the product page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Scrape price from an Amazon page (change to match the target page)
    price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()  # You can adjust this as per the website you're scraping

    # Check if the price is in USD, and convert it to INR
    if price.startswith('$'):  # If price is in USD
        price_in_usd = float(price[1:])  # Remove '$' and convert to float
        price_in_inr = price_in_usd * USD_TO_INR  # Convert USD to INR using the conversion rate
    else:
        # If the price is already in INR, return it as it is
        price_in_inr = float(price[1:])  # Assuming price is in INR, remove the currency symbol and convert to float

    return price_in_inr
