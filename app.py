import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your existing data
vestibulares_data = {
    "ENEM": {
        "date": "3 e 10 de novembro de 2024",
        "fee": "R$ 85,00",
        "official_website": "https://enem.inep.gov.br/",
        "phases": 1
    },
    "FUVEST": {
        "date": "15 de janeiro de 2024",
        "fee": "R$ 190,00",
        "official_website": "https://www.fuvest.br/",
        "phases": 2
    },
    "UNICAMP": {
        "date": "12 de dezembro de 2023",
        "fee": "R$ 190,00",
        "official_website": "https://www.comvest.unicamp.br/",
        "phases": 2
    },
}

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    response = chatbot_response(user_message)
    return jsonify({"response": response})

def chatbot_response(user_input):
    # Custom response logic
    return "Eu não entendi sua pergunta."

if __name__ == '__main__':
    # Use the PORT environment variable if available
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not provided
    app.run(host="0.0.0.0", port=port, debug=True)
