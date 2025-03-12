import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }

    try:
        # Set a timeout of 15 seconds for the request
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=15)

        # Log the status code and first 500 characters of the HTML content
        print(f"Status code: {response.status_code}")
        print(f"Response Body (first 500 characters): {response.text[:500]}")

        # If the response is not successful, raise an exception
        response.raise_for_status()

        # Check if the content is correct (not empty or containing an error message)
        if "robot check" in response.text.lower():
            raise ValueError("The request was blocked, possibly by a bot protection mechanism.")

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try different possible price selectors
        price_tag = soup.find('span', {'class': 'a-price-whole'})  # Amazon price selector
        if not price_tag:
            # Try other possible selectors if the main one is not found
            price_tag = soup.find('span', {'id': 'priceblock_ourprice'})  # Another possible selector
        
        if not price_tag:
            # Try the new price formatting for "a-price-symbol" class
            price_tag = soup.find('span', {'class': 'a-price-symbol'}) 

        if price_tag:
            # Clean up the price string, remove unwanted characters
            price = price_tag.text.strip().replace(',', '').replace('₹', '')
            print(f"Price found: ₹{price}")
            return float(price)  # Return the price as a float
        else:
            raise ValueError("Could not find the price on the page.")

    except requests.exceptions.RequestException as e:
        # Catch network or request errors (e.g., 404, 500, timeouts)
        print(f"Request error: {e}")
        raise ValueError("Failed to retrieve the page. Please check the URL.")

    except ValueError as e:
        # Catch missing or incorrect price errors
        print(f"Value error: {e}")
        raise ValueError("Could not extract price. Please check the page structure or URL.")

    except Exception as e:
        # Catch any unforeseen errors and log the exception
        print(f"An error occurred: {e}")
        raise ValueError("An unexpected error occurred while scraping the price.")
