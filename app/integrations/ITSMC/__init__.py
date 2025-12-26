import requests

def generate_incident():
    # URL da API
    url_api = "https://viacep.com.br/ws/01001000/json/"
    
    # Faz a requisição GET
    resposta = requests.get(url_api)

    # Verifica se a requisição foi bem-sucedida (código 200)
    if resposta.status_code == 200:
        dados_json = resposta.json() # Converte a resposta JSON para um dicionário Python
        print("Dados recebidos:")
        return f"I2512-{dados_json["siafi"]}"
    else:
        print(f"Erro: {resposta.status_code}")
        return "Não Gerado"
        