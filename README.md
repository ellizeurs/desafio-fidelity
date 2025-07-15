# Desafio Fidelity
Repositório criado para resolução do desafio técnico do processo seletivo da Fidelity Pesquisas Cadastrais.

## Uso
1. Clone o repositório para o seu arquivo local
````bash
https://github.com/ellizeurs/desafio-fidelity.git
````
2. Entre na pasta do repositório
````bash
cd desafio-fidelity
````
3. Crie o arquivo ```.env``` a partir do exemplo 
````bash
cp .env.example .env
````
> O arquivo de exemplo está com as variáveis dadas pelo desafio
4. Crie e entre no ambiente virtual python (opcional)
````bash
python -m venv venv
source venv/bin/activate #Linux
venv/src/activate # Windows
````
5. Instale as bibliotecas
````bash
pip install -r requirements.txt
````
6. Execute a função principal
````bash
python src/main.py
````

---
Por Ellizeu Sena