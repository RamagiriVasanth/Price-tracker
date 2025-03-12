import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    # Define headers to avoid being blocked by the website's bot protection
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }

    try:
        # Send GET request with a timeout to avoid hanging
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)

        # Log the status code and first 500 characters of the HTML content for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response Body (first 500 characters): {response.text[:500]}")

        # Raise an exception for bad responses (404, 500, etc.)
        response.raise_for_status()

        # Handle cases where the website might have bot protection
        if "robot check" in response.text.lower():
            raise ValueError("The request was blocked, possibly by a bot protection mechanism.")

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple selectors to find the price depending on the website structure
        price_tag = soup.find('span', {'class': 'a-price-whole'})  # Amazon main price selector
        if not price_tag:
            price_tag = soup.find('span', {'id': 'priceblock_ourprice'})  # Another Amazon price selector

        if not price_tag:
            price_tag = soup.find('span', {'class': 'a-price-symbol'})  # For deal prices on Amazon

        if not price_tag:
            price_tag = soup.find('span', {'id': 'priceblock_dealprice'})  # Amazon Deal Price tag

        if not price_tag:
            price_tag = soup.find('span', {'class': 'price'})  # Common class for various websites' price tags

        if not price_tag:
            price_tag = soup.find('span', {'class': 'product-price'})  # Fallback for other common websites

        if not price_tag:
            raise ValueError("Could not find the price on the page. Please check the page structure or URL.")

        # Extract and clean the price
        price_text = price_tag.get_text(strip=True).replace(',', '').replace('₹', '').replace('$', '')
        print(f"Price found: ₹{price_text}")

        # Convert to float and return the price
        return float(price_text)

    except requests.exceptions.RequestException as e:
        # Handle network issues, timeouts, invalid URLs, etc.
        print(f"Request error: {e}")
        raise ValueError("Failed to retrieve the page. Please check the URL and your internet connection.")

    except ValueError as e:
        # Handle missing or invalid price errors
        print(f"Value error: {e}")
        raise ValueError("Could not extract price. Please check the page structure or URL.")

    except Exception as e:
        # Catch unforeseen errors and log them
        print(f"An error occurred: {e}")
        raise ValueError("An unexpected error occurred while scraping the price.")
