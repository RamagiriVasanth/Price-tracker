import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Set a timeout of 10 seconds for the request
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        # Log the status code and first 500 characters of the HTML content
        print(f"Status code: {response.status_code}")
        print(f"Response Body (first 500 characters): {response.text[:500]}")

        # Raise an error for HTTP errors
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape price from the page
        price_tag = soup.find('span', {'class': 'a-price-whole'})  # Amazon-specific selector
        if price_tag:
            price = price_tag.text.strip().replace(',', '')  # Clean up the price string
            print(f"Price found: ₹{price}")
            return float(price)  # Convert to float
        else:
            raise ValueError("Could not find the price on the page")

    except requests.exceptions.RequestException as e:
        # Catch network or request errors (e.g., 404, 500)
        print(f"Request error: {e}")
        raise ValueError("Failed to retrieve the page. Please check the URL.")
    
    except ValueError as e:
        # Catch missing or incorrect price errors
        print(f"Value error: {e}")
        raise ValueError("Could not extract price. Please check the page structure or URL.")
    
    except Exception as e:
        # Catch any other unforeseen errors
        print(f"An error occurred: {e}")
        raise ValueError("An unexpected error occurred while scraping the price.")
