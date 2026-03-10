1 - Clone o repositório:

# git clone https://github.com/alexsbcorrea/api-service-desk-agent-python-v4.git

2 - Abra o repositório no Visual Studio Code;

3 - Crie uma ambiente virtual para instalar as dependências do projeto;

# python -m venv venv

3 - Ative o ambiente virtual

# Windows

# .\venv\Scripts\activate.ps1

# Linux

# source venv/bin/activate

4 - Instale as dependências do projeto

# pip install -r requirements.txt

5 - Inicialize o setup de Migração
# flask db init

6 - Crie a primeira migração
# flask db migrate -m "inicio"

7 - Execute a primeira migração
# flask db upgrade

5 - Execute o projeto

# python run.py
