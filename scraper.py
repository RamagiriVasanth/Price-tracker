import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    # Define the headers to avoid being blocked by the website's bot protection
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }

    try:
        # Send the GET request with a 30-second timeout to avoid hanging
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)

        # Log the status code and first 500 characters of the HTML content for debugging
        print(f"Status code: {response.status_code}")
        print(f"Response Body (first 500 characters): {response.text[:500]}")

        # Raise an exception for bad responses (404, 500, etc.)
        response.raise_for_status()

        # If the response contains any bot protection message (e.g., "robot check"), handle it
        if "robot check" in response.text.lower():
            raise ValueError("The request was blocked, possibly by a bot protection mechanism.")

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple selectors to find the price, depending on the website structure
        price_tag = soup.find('span', {'class': 'a-price-whole'})  # Amazon price selector
        if not price_tag:
            price_tag = soup.find('span', {'id': 'priceblock_ourprice'})  # Another common Amazon selector
        
        if not price_tag:
            price_tag = soup.find('span', {'class': 'a-price-symbol'})  # Amazon deal prices
        
        if not price_tag:
            price_tag = soup.find('span', {'id': 'priceblock_dealprice'})  # For Amazon Deal Price

        if not price_tag:
            price_tag = soup.find('span', {'class': 'price'})  # Common price class for various sites

        # If the price tag is found, extract and clean the price
        if price_tag:
            # Extract the price and clean up any unwanted characters (like ₹, $, commas)
            price_text = price_tag.get_text(strip=True).replace(',', '').replace('₹', '').replace('$', '')
            print(f"Price found: ₹{price_text}")

            # Convert to float and return the price
            return float(price_text)

        else:
            # Raise an error if no price is found
            raise ValueError("Could not find the price on the page. Please check the page structure or URL.")

    except requests.exceptions.RequestException as e:
        # Handle errors like network issues, timeout, invalid URLs, etc.
        print(f"Request error: {e}")
        raise ValueError("Failed to retrieve the page. Please check the URL and your internet connection.")

    except ValueError as e:
        # Handle missing or invalid price extraction errors
        print(f"Value error: {e}")
        raise ValueError("Could not extract price. Please check the page structure or URL.")

    except Exception as e:
        # Catch any unforeseen errors and log them
        print(f"An error occurred: {e}")
        raise ValueError("An unexpected error occurred while scraping the price.")
