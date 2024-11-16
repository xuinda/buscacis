import os
import pandas as pd
from flask import Flask, request, jsonify

# Inicializando o Flask
app = Flask(__name__)

# Rota básica para verificar se o servidor está funcionando
@app.route('/')
def home():
    return "Servidor Flask está funcionando!"

# Rota para buscar CI (no caso do chatbot) a partir de um arquivo .xlsx
@app.route('/buscar_ci', methods=['GET'])
def buscar_ci():
    # Pega o termo de busca do parâmetro da URL
    termo = request.args.get('termo', '')
    
    # Caminho do arquivo Excel, utilizando variável de ambiente
    caminho_arquivo = os.getenv('CAMINHO_ARQUIVO', 'saida.xlsx')  # 'saida.xlsx' é o valor padrão
    
    try:
        # Carregando o arquivo Excel (.xlsx) com pandas
        df = pd.read_excel(caminho_arquivo)
        
        # Filtrando os resultados que contêm o termo de busca na coluna 'conteudo'
        resultados = df[df['conteudo'].str.contains(termo, case=False, na=False)]
        
        # Retorna os resultados como uma resposta JSON
        return jsonify(resultados[['nome_arquivo', 'conteudo']].to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Obtém a porta do ambiente ou usa 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    
    # Configura o Flask para escutar na porta correta
    app.run(host='0.0.0.0', port=port)
