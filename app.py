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
    try:
        current_price = scrape_price(product_url)
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)})

    tracked_products.append({
        'url': product_url,
        'target_price': target_price,
        'current_price': current_price
    })

    # Check if the price is below or equal to the target price
    if current_price <= target_price:
        # Price alert triggered
        return jsonify({
            'success': True,
            'message': f"Price alert! The price of {product_url} has dropped to ₹{current_price}. Tracking started."
        })
    else:
        # Price tracking started but no alert triggered
        return jsonify({
            'success': True,
            'message': f"Price tracking started for {product_url}. Current price: ₹{current_price}. Waiting for price drop."
        })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Use the port provided by Render or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
