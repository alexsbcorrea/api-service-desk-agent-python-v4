from .classify_intent import classify_intent


def handle_message(message: str) -> str:
    intent = classify_intent(message)
    
    print(intent)

    if intent == "saudacao":
        return ("Olá! Sou o assistente virtual do Service Desk. Como posso te ajudar hoje?\n"
                "1️⃣ Problemas de acesso (senha, login, VPN)\n2️⃣ Aplicativos e sistemas\n"
                "3️⃣ Equipamentos (notebook, impressora, periféricos)\n4️⃣ Solicitação de software ou acesso\n"
                "5️⃣ Falar com um atendente")
    elif intent == "senha_ad":
        return "A sua senha de Rede (AD) fornece acesso aos computadores, E-mail e aos portais RH Net, Service Desk (TopDesk) e Portal de Ponto. Para alterar a sua senha acesse: https://passwordreset.microsoftonline.com/"
    elif intent == "senha_tasy":
        return "Para alterar a senha do Tasy é necessário entrar em contato com o atendimento."
    elif intent == "feedback":
        return "Obrigado pelo contato."
        #return request_feedback(user_id)
    else:
        # Fallback para N1 (humano) — aqui ainda mock
        return "Você será direcionado para um atendente."
