from flask import Flask, request, jsonify
import pandas as pd

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
    
    # Caminho completo do arquivo Excel
    caminho_arquivo = r'D:\RICARDO\esquemas txt\app\saida.xlsx'  # Substitua pelo seu caminho exato
    
    try:
        # Carregando o arquivo Excel (.xlsx) com pandas
        df = pd.read_excel(caminho_arquivo)  # Carrega o arquivo Excel
        
        # Verificando as colunas disponíveis
        print("Colunas encontradas:", df.columns.tolist())
        
        # Verificando se a coluna 'conteudo' existe
        if 'conteudo' not in df.columns:
            return jsonify({"error": "A coluna 'conteudo' não foi encontrada no arquivo Excel."}), 400
        
        # Filtrando os resultados que contêm o termo de busca na coluna 'conteudo'
        resultados = df[df['conteudo'].str.contains(termo, case=False, na=False)]
        
        # Se não houver resultados, retornar uma mensagem apropriada
        if resultados.empty:
            return jsonify({"message": "Nenhum resultado encontrado."}), 404
        
        # Retorna os resultados como uma resposta JSON
        return jsonify(resultados[['nome_arquivo', 'conteudo']].to_dict(orient='records'))
    
    except Exception as e:
        # Caso ocorra algum erro, retorna a mensagem de erro
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
