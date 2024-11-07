from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS to allow cross-origin requests

app = Flask(__name__)
CORS(app, origins=["*"])   # Allow cross-origin requests

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

# Function to get data for a specific exam
def get_vestibular_info(exam_name):
    exam_name = exam_name.upper()
    if exam_name in vestibulares_data:
        return vestibulares_data[exam_name]
    else:
        return {"error": "Vestibular not found"}

# Function for chatbot response
def chatbot_response(user_input):
    if "all exams" in user_input.lower():
        response = "Aqui estão os vestibulares disponíveis:\n"
        for exam, details in vestibulares_data.items():
            response += f"{exam}: {details['date']}, Taxa: {details['fee']}, Fases: {details['phases']}\n"
        return response
    else:
        for exam in vestibulares_data:
            if exam.lower() in user_input.lower():
                exam_info = get_vestibular_info(exam)
                if "error" in exam_info:
                    return "Desculpe, não encontrei as informações sobre esse vestibular."
                else:
                    return (
                        f"{exam} Detalhes:\n"
                        f"Data: {exam_info['date']}\n"
                        f"Taxa: {exam_info['fee']}\n"
                        f"Website Oficial: {exam_info['official_website']}\n"
                        f"Fases: {exam_info['phases']}\n"
                    )
        return "Não entendi qual vestibular você está perguntando. Por favor, mencione 'ENEM', 'FUVEST' ou 'UNICAMP'."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    response = chatbot_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

