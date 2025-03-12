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
    target_price = float(data['price'])  # The target price provided by the user

    # Scrape the product price from the given URL
    try:
        current_price = scrape_price(product_url)

        tracked_products.append({
            'url': product_url,
            'target_price': target_price,
            'current_price': current_price
        })

        # Send an alert if the price is below or equal to the target price
        if current_price <= target_price:
            send_alert(product_url, current_price)

        return jsonify({'success': True, 'message': 'Price tracking started!'})
    
    except ValueError as e:
        # Catch any errors from the scraper and send a helpful message back
        return jsonify({'success': False, 'message': str(e)})

def send_alert(product_url, current_price):
    try:
        account_sid = 'your_account_sid'  # Replace with your Twilio SID
        auth_token = 'your_auth_token'  # Replace with your Twilio auth token
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f'Price alert! The product at {product_url} is now at ₹{current_price:.2f}',  # Send price in INR (₹)
            from_='+1234567890',  # Replace with your Twilio number
            to='+0987654321'      # Replace with the user's phone number
        )

        print(f"Message sent: {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Use the port provided by Render or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
