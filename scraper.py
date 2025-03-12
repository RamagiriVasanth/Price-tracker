import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape price from an Amazon page (adjust based on your target page structure)
        price_tag = soup.find('span', {'class': 'a-price-whole'})  # Modify based on the actual page structure
        if price_tag:
            price = price_tag.text.strip().replace(',', '')  # Clean up the price string
            return float(price)  # Convert to float (remove ₹ symbol if necessary)
        else:
            raise ValueError("Could not find the price on the page")
    
    except requests.exceptions.RequestException as e:
        # Log any request exceptions (e.g. network issues, page not found)
        print(f"Request error: {e}")
        raise ValueError("Failed to retrieve the page. Please check the URL.")
    except ValueError as e:
        # Log any value errors (e.g. couldn't find the price element)
        print(f"Value error: {e}")
        raise ValueError("Could not extract price. Please check the page structure or URL.")
    except Exception as e:
        # Catch any other exceptions
        print(f"An error occurred: {e}")
        raise ValueError("An unexpected error occurred while scraping the price.")
