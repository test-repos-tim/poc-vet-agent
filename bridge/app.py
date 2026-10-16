# bridge/app.py
from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load knowledge base
KB_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'vet_knowledge_base.json')
with open(KB_PATH) as f:
    KB = json.load(f)

def get_bot_reply(user_message):
    """Simple rule-based reply based on knowledge base (placeholder for Hermes agent)"""
    lower = user_message.lower()
    # FAQ matching
    for faq in KB['faqs']:
        if any(word in lower for word in faq['question'].lower().split()):
            return faq['answer']
    # Default responses
    if any(word in lower for word in ['hello', 'hi', 'hey']):
        return 'Hello! I am the virtual assistant for Paws & Claws Animal Hospital. How can I help your pet today?'
    if any(word in lower for word in ['appoint', 'book', 'schedule']):
        return 'I can help you book an appointment. Please provide: pet name, species, preferred date/time, and reason for visit.'
    if any(word in lower for word in ['emergency', 'urgent']):
        return 'If this is an emergency, please call us immediately at (555) 123-4567 or bring your pet to our clinic.'
    if any(word in lower for word in ['prescription', 'refill', 'medication']):
        return 'For prescription refills, please provide: pet name, medication name, dosage, and your pharmacy contact.'
    if any(word in lower for word in ['hour', 'open', 'time']):
        return 'Our hours are Monday-Friday 8am-8pm, Saturday 9am-5pm. Closed Sundays.'
    return 'I am still learning. For urgent questions, please call (555) 123-4567. I can help with appointments, hours, and prescription refills.'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    bot_reply = get_bot_reply(user_message)
    # Log conversation (optional)
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user': user_message,
        'bot': bot_reply
    }
    print(f"[{log_entry['timestamp']}] User: {user_message}")
    print(f"[{log_entry['timestamp']}] Bot: {bot_reply}")
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)