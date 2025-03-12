from flask import Flask, render_template, request, jsonify
from scraper import scrape_price  # Import the scraper

app = Flask(__name__)

tracked_products = []  # Store tracked products

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track-price', methods=['POST'])
def track_price():
    data = request.json  # Parse the incoming JSON data from the request

    # Validate URL and price fields
    if 'url' not in data or 'price' not in data:
        return jsonify({'success': False, 'message': 'Missing url or price parameter.'})

    try:
        # Ensure that price is a valid float and URL is valid
        product_url = data['url']
        target_price = float(data['price'])  # Convert target price to float
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid price value.'})

    # Scrape the product price from the URL using the scraper function
    try:
        current_price = scrape_price(product_url)
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'message': 'An unexpected error occurred while retrieving the price.'})

    # Add product to tracked list if price scraping is successful
    tracked_products.append({
        'url': product_url,
        'target_price': target_price,
        'current_price': current_price
    })

    # Check if the product's current price is less than or equal to the target price
    if current_price <= target_price:
        send_alert(product_url, current_price)

    return jsonify({'success': True, 'message': 'Price tracking started!'})

def send_alert(product_url, current_price):
    """Simulate alert (for logging or browser notification)"""
    print(f"ALERT: The price of the product at {product_url} is now ₹{current_price}.")
    # You can replace the print with actual alert notifications or email notifications.

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment variable or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
