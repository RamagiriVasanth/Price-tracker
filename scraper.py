import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.amazon.in"  # Adding referer to make the request look more legitimate
    }
    
    try:
        # Sending the request to the product URL
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()  # This will raise an exception for HTTP errors (e.g., 404, 500)
        
        # Debugging: Print the raw HTML response (first 500 characters)
        print("Page content preview:", response.text[:500])  # Preview of the HTML content
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape the price (modify based on the actual page structure)
        price_tag = soup.find('span', {'class': 'a-price-whole'})  # Update this if the class changes

        # If price_tag is found, clean the price value
        if price_tag:
            price = price_tag.text.strip().replace(',', '')  # Remove commas and extra spaces
            return float(price)  # Return as float (ignoring ₹ symbol, if present)
        else:
            raise ValueError("Could not find the price on the page")

    except requests.exceptions.RequestException as e:
        # This will handle network issues, invalid URL, timeouts, etc.
        print(f"Request error: {e}")
        raise ValueError("Failed to retrieve the page. Please check the URL.")

    except ValueError as e:
        # This will handle any issues with extracting the price
        print(f"Value error: {e}")
        raise ValueError("Could not extract price. Please check the page structure or URL.")
    
    except Exception as e:
        # Catch all other exceptions and print the error
        print(f"An unexpected error occurred: {e}")
        raise ValueError("An unexpected error occurred while scraping the price.")
