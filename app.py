from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Iski wajah se "Failed to Fetch" nahi aayega

def get_bot_response(user_message):
    message = user_message.lower()
    if "hello" in message or "hi" in message or "assalam" in message:
        return "Walaikum Assalam! Solar Cleaning Service me khush aamdeed. Mein aapki kya madad kar sakta hoon?"
    elif "service" in message or "cleaning" in message:
        return "Hum 4 qism ki services dete hain: Home Cleaning, Commercial Cleaning, Dry Cleaning, aur Emergency Cleaning."
    elif "price" in message or "rate" in message or "fees" in message:
        return "Humari cleaning Rs. 50 se Rs. 100 per panel tak hoti hai, depending on service type."
    elif "book" in message or "order" in message:
        return "Booking karne ke liye aap hamari website ke Booking section me ja kar form fill kar sakte hain!"
    else:
        return "Maazrat, mujhe samajh nahi aaya. Kya aap Solar Cleaning, Prices, ya Booking ke baare me poochna chahte hain?"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    user_text = data['message']
    bot_reply = get_bot_response(user_text)
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)