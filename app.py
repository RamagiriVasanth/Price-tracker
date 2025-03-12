from flask import Flask, render_template, request, jsonify
from scraper import scrape_price  # Import the scraper
from twilio.rest import Client

app = Flask(__name__)

tracked_products = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track-price', methods=['POST'])
def track_price():
    data = request.json
    product_url = data['url']
    target_price = float(data['price'])

    # Scrape the product price
    current_price = scrape_price(product_url)

    tracked_products.append({
        'url': product_url,
        'target_price': target_price,
        'current_price': current_price
    })

    if current_price <= target_price:
        send_alert(product_url, current_price)

    return jsonify({'success': True})

def send_alert(product_url, current_price):
    account_sid = 'your_account_sid'  # Replace with your Twilio SID
    auth_token = 'your_auth_token'  # Replace with your Twilio auth token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Price alert! The product at {product_url} is now at ₹{current_price:.2f}',  # Send price in INR (₹)
        from_='+1234567890',  # Replace with your Twilio number
        to='+0987654321'      # Replace with the user's phone number
    )

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
