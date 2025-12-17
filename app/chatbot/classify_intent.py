import json
import re
from pathlib import Path
import os

def classify_intent(message: str):
    
    diretorio_atual = os.getcwd()
    intents_file_path = os.path.join(diretorio_atual,"app","chatbot", "intents_file.json")
    
    with open(intents_file_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    mensagem_lower = message.lower()
    
    intentions_on_message = []

    for intent in dados["intents"]:
        for palavra in intent["keywords"]:
            if palavra in mensagem_lower:
                intentions_on_message.append(intent["name"])
    
    print(intentions_on_message)
    
    if len(intentions_on_message) == 0:
        return "intencao_desconhecida"
    
    if len(intentions_on_message) > 1 and "saudacao" in intentions_on_message:
        intentions_on_message.remove("saudacao")

    print("RESULT: ", intentions_on_message[0])
    return intentions_on_message[0]