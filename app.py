from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import difflib  # Close matching aur spelling tolerance ke liye

app = Flask(__name__)
CORS(app)

# English Knowledge Base tailored for your database schema
KNOWLEDGE_BASE = {
    "hello": "Hello! Welcome to Smart Solar Wash. How can I assist you with your solar panels today?",
    "hi": "Hi there! Welcome to Smart Solar Wash. How can I help you today?",
    "cleaning": "We provide 4 premium services: Home Cleaning (Rs. 50/panel), Commercial Cleaning (Rs. 80/panel), Dry Cleaning (Rs. 70/panel), and Emergency Cleaning (Rs. 100/panel).",
    "services": "Our core services include Residential Rooftop, Industrial/Commercial, Waterless Dry Cleaning, and urgent Emergency panel dust removal.",
    "price": "Our standard professional rates vary from Rs. 50 up to Rs. 100 per panel based on your selected cleaning service type.",
    "rates": "Affordable rates: Home Cleaning is Rs. 50, Dry Cleaning is Rs. 70, Commercial is Rs. 80, and Emergency response is Rs. 100 per solar panel.",
    "booking": "To book a cleaning slot, please visit the 'Book Cleaning' section in the website menu and fill out the quick details form.",
    "calculator": "You can dynamically estimate your total budget by using our 'Cost Calculator' page built directly into the web platform.",
    "contact": "You can email us at info@solarclean.com or call our helpline at +92 337 8568026. We operate all over Pakistan.",
    "location": "We are currently operational and offering premium solar cleaning setups across major cities in Pakistan.",
    "thanks": "You're very welcome! Feel free to ask if you have any other questions regarding our solar solutions.",
    "thank you": "You're welcome! Let me know if you need anything else to optimize your solar output."
}

def get_intelligent_response(user_message):
    tokens = user_message.lower().strip().split()
    if not tokens:
        return "I didn't quite catch that. Could you please type your question clearly?"

    keywords = list(KNOWLEDGE_BASE.keys())
    
    # 1. Individual word level token checking with 70% spell match criteria
    for token in tokens:
        matches = difflib.get_close_matches(token, keywords, n=1, cutoff=0.7)
        if matches:
            return KNOWLEDGE_BASE[matches[0]]
            
    # 2. Whole phrase level match with 60% tolerance threshold
    phrase_matches = difflib.get_close_matches(user_message.lower(), keywords, n=1, cutoff=0.6)
    if phrase_matches:
        return KNOWLEDGE_BASE[phrase_matches[0]]

    # General Fallback Response for completely out-of-context inputs
    return "Thank you for reaching out! I am specialized in answering queries related to our Solar Services, Pricing Plans, Cost Estimation, and Booking. Could you please specify your query about these topics?"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
        
    user_text = data['message']
    bot_reply = get_intelligent_response(user_text)
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
