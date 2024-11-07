import requests
from datetime import datetime

# Function to get the vestibular info from the API
def get_vestibular_info(exam_name):
    url = f"http://127.0.0.1:5000/vestibulares/{exam_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Vestibular não encontrado"}

# Function to get all vestibulares data from the API
def get_all_vestibulares():
    url = "http://127.0.0.1:5000/vestibulares"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {"error": "Não foi possível recuperar os vestibulares"}

# Function to handle the chatbot response logic
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Basic communication responses
    if "olá" in user_input or "oi" in user_input:
        return "Olá! Como posso ajudá-lo hoje?"
    elif "como está" in user_input:
        return "Estou bem, obrigado por perguntar! Qual vestibular você irá prestar?"
    elif "qual é o dia" in user_input or "que dia é hoje" in user_input:
        today = datetime.today().strftime('%d/%m/%Y')
        return f"Hoje é {today}."

    # Handling requests for all vestibulares
    elif "todos os vestibulares" in user_input:
        vestibulares = get_all_vestibulares()
        response = "Aqui estão os vestibulares disponíveis:\n"
        for exam, details in vestibulares.items():
            response += f"{exam}: {details['date']}, Taxa: {details['fee']}, Fases: {details['phases']}\n"
        return response

    # Handling specific exam inquiries
    else:
        for exam in ["ENEM", "FUVEST", "UNICAMP"]:
            if exam.lower() in user_input:
                exam_info = get_vestibular_info(exam)
                if "error" in exam_info:
                    return "Desculpe, não encontrei informações sobre esse vestibular."
                else:
                    # Check if the user is asking for the date only
                    if "data" in user_input:
                        return f"A data do {exam} é: {exam_info['date']}."
                    else:
                        return (
                            f"Detalhes do {exam}:\n"
                            f"Data: {exam_info['date']}\n"
                            f"Taxa: {exam_info['fee']}\n"
                            f"Site oficial: {exam_info['official_website']}\n"
                            f"Fases: {exam_info['phases']}\n"
                        )
        return "Desculpe, não entendi qual vestibular você está perguntando. Por favor, especifique 'ENEM', 'FUVEST' ou 'UNICAMP'."

# Example of user input and response
user_input = "Qual é a data da FUVEST?"
print(chatbot_response(user_input))

