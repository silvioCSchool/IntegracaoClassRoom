from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Define os escopos de autorização para acessar o Google Classroom
SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students', 'https://www.googleapis.com/auth/classroom.courses.readonly']

# Função para autenticar e conectar ao Google Classroom usando OAuth2
def obter_servico_classroom():
    credenciais = None
    # Verifica se o token já existe para reutilizar as credenciais
    if os.path.exists('token.json'):
        credenciais = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        # Autenticação via OAuth2
        fluxo = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credenciais = fluxo.run_local_server(port=8081, prompt='consent')
        # Salva o token para reutilização futura
        with open('token.json', 'w') as token:
            token.write(credenciais.to_json())

    # Constrói o serviço Google Classroom usando as credenciais
    servico = build('classroom', 'v1', credentials=credenciais)
    return servico

# Função para validar se o curso existe
def validar_curso(servico, courseId):
    try:
        # Faz a requisição para obter os detalhes do curso
        curso = servico.courses().get(id=courseId).execute()
        print(f"Curso encontrado: {curso['name']} (ID: {curso['id']})")
        return True  # Curso encontrado
    except Exception as e:
        print(f"Erro ao acessar o curso: {str(e)}")
        return False  # Curso não encontrado

# Rota da API que recebe os dados da atividade e posta no Google Classroom
@app.route('/criar_atividade', methods=['POST'])
def criar_atividade():
    try:
        # Obtém os dados do JSON enviados no corpo da requisição
        dados = request.get_json()
        titulo = dados['titulo']
        descricao = dados['descricao']
        alternativas = dados['alternativas']
        resposta_correta = dados['resposta_correta']
        id_curso = dados['id_curso']  # ID do curso no Google Classroom
        
        # Verifica se há exatamente 5 alternativas
        if len(alternativas) != 5:
            return jsonify({'erro': 'Deve haver exatamente 5 alternativas'}), 400

        # Conecta ao serviço Google Classroom
        servico = obter_servico_classroom()

        # Valida se o curso existe
        if not validar_curso(servico, id_curso):
            return jsonify({'erro': f'Curso com ID {id_curso} não encontrado'}), 404

        # Define o corpo da questão que será enviada ao Google Classroom
        atividade = {
            'title': titulo,  # Título da atividade
            'description': descricao,  # Descrição ou enunciado da pergunta
            'workType': 'MULTIPLE_CHOICE_QUESTION',  # Tipo de questão de múltipla escolha
            'state': 'PUBLISHED',  # Define que a questão será publicada imediatamente
            'multipleChoiceQuestion': {
                'choices': alternativas  # Lista de alternativas de resposta
            },
            'maxPoints': 10,  # Define a pontuação máxima para a pergunta
        }

        # Envia a atividade ao Google Classroom para o curso especificado
        resposta = servico.courses().courseWork().create(courseId=id_curso, body=atividade).execute()

        # Retorna uma mensagem de sucesso com o ID da atividade criada
        return jsonify({'mensagem': 'Atividade criada com sucesso!', 'id': resposta['id']})
    
    except Exception as e:
        # Retorna a mensagem de erro caso algo falhe no processo
        return jsonify({'erro': str(e)}), 500

# Rota de exemplo para verificar se a API está rodando
@app.route('/', methods=['GET'])
def index():
    return "API do Google Classroom para criar atividades está funcionando!"

# Inicializa o servidor Flask na porta 8080
if __name__ == '__main__':
    app.run(debug=True, port=8080)
