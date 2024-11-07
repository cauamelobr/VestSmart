from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS to enable cross-origin requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Vestibulares data
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

# Function to retrieve specific vestibular info
def get_vestibular_info(exam_name):
    exam_name = exam_name.upper()
    return vestibulares_data.get(exam_name, {"error": "Vestibular não encontrado"})

# Function to generate chatbot response
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Handle requests for all exams
    if "todos os vestibulares" in user_input:
        response = "Aqui estão os vestibulares disponíveis:\n"
        for exam, details in vestibulares_data.items():
            response += f"{exam}: {details['date']}, Taxa: {details['fee']}, Fases: {details['phases']}\n"
        return response

    # Check for specific exam inquiries
    for exam, details in vestibulares_data.items():
        if exam.lower() in user_input:
            if "data" in user_input:
                return f"A data do {exam} é: {details['date']}."
            else:
                return (
                    f"Detalhes do {exam}:\n"
                    f"Data: {details['date']}\n"
                    f"Taxa: {details['fee']}\n"
                    f"Site oficial: {details['official_website']}\n"
                    f"Fases: {details['phases']}\n"
                )

    # Handle greetings and common questions
    if any(greeting in user_input for greeting in ["olá", "oi", "como está"]):
        return "Olá! Como posso ajudá-lo hoje?"

    if "qual é o dia" in user_input or "que dia é hoje" in user_input:
        from datetime import datetime
        today = datetime.today().strftime('%d/%m/%Y')
        return f"Hoje é {today}."

    return "Desculpe, não entendi sua pergunta. Por favor, pergunte sobre um vestibular específico."

# Endpoint for the chatbot to respond to user messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    response = chatbot_response(user_message)
    return jsonify({"response": response})

# Run the Flask app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)


