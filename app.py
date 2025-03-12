from flask import Flask, render_template, request, jsonify
from scraper import scrape_price  # Import the scraper

app = Flask(__name__)

tracked_products = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track-price', methods=['POST'])
def track_price():
    data = request.json
    product_url = data['url']
    target_price = float(data['price'])  # The target price provided by the user

    # Scrape the product price from the given URL
    current_price = scrape_price(product_url)

    tracked_products.append({
        'url': product_url,
        'target_price': target_price,
        'current_price': current_price
    })

    if current_price <= target_price:
        send_alert(product_url, current_price)

    return jsonify({'success': True, 'message': 'Price tracking started!'})

# Simulated Alert Function (Instead of using Twilio)
def send_alert(product_url, current_price):
    # Simulate an alert by printing the message to the console (or you can log it or store in DB)
    print(f"Price alert! The product at {product_url} is now at ₹{current_price:.2f}")
    # Or, if you want to return an alert to the frontend, you can use:
    # return jsonify({'success': True, 'alert': f'Price alert! The product at {product_url} is now at ₹{current_price:.2f}'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Use the port provided by Render or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
