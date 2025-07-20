from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Vamos armazenar o estado da conversa em memória para o exemplo simples (em produção use DB)
user_states = {}
user_data = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    sender = request.form.get('From')  # número do usuário
    msg = request.form.get('Body').strip().lower()
    resp = MessagingResponse()

    state = user_states.get(sender, "START")

    if state == "START":
        if "denunciar" in msg:
            user_states[sender] = "ASK_TYPE"
            resp.message(
                "Obrigado por usar nosso serviço de denúncias.\nPor favor, envie o tipo da denúncia:\n"
                "1️⃣ Spam\n2️⃣ Conteúdo impróprio\n3️⃣ Fraude\n4️⃣ Outro"
            )
        else:
            resp.message("Olá! Para fazer uma denúncia, envie uma mensagem contendo a palavra 'denunciar'.")
    
    elif state == "ASK_TYPE":
        types = {"1": "Spam", "2": "Conteúdo impróprio", "3": "Fraude", "4": "Outro"}
        if msg in types:
            user_data[sender] = {"type": types[msg]}
            user_states[sender] = "ASK_DETAILS"
            resp.message(f"Você escolheu '{types[msg]}'. Por favor, descreva a denúncia com detalhes.")
        else:
            resp.message("Opção inválida. Por favor, envie um número de 1 a 4 correspondente ao tipo de denúncia.")
    
    elif state == "ASK_DETAILS":
        user_data[sender]["details"] = msg
        # Aqui você pode salvar user_data[sender] no banco ou enviar para equipe
        resp.message("Denúncia recebida com sucesso! Nossa equipe irá analisar e entrar em contato se necessário. Obrigado.")
        # Resetar estado para permitir nova denúncia depois
        user_states[sender] = "START"
        user_data.pop(sender, None)

    else:
        user_states[sender] = "START"
        resp.message("Olá! Para fazer uma denúncia, envie uma mensagem contendo a palavra 'denunciar'.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
