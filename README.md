
# Integração com Google Classroom

Este projeto implementa uma integração com o Google Classroom para permitir a criação de atividades e a listagem de cursos. Ele utiliza Flask para expor uma API RESTful e a biblioteca Google API Client para interação com os serviços do Google.

## Estrutura do Projeto

- **`credentials.json`**: Arquivo de credenciais para autenticação com a API do Google.
- **`token.json`**: Gerado automaticamente após a autenticação inicial, contendo o token de acesso.
- **`integracao.py`**: Código principal contendo a API Flask para criar atividades no Google Classroom.
- **`listarCursos.py`**: Script para listar os cursos disponíveis na conta do Google Classroom autenticada.

---

## Funcionalidades

### Listar Cursos
Permite consultar os cursos disponíveis na conta autenticada.

### Criar Atividades
Adiciona atividades de múltipla escolha a um curso específico no Google Classroom.

---

## Pré-requisitos

- Python 3.8 ou superior
- Conta Google com acesso ao Google Classroom
- Dependências Python:
  ```bash
  pip install flask google-auth google-auth-oauthlib google-api-python-client
  ```

---

## Configuração do Ambiente

1. **Ativar API do Google Classroom**:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
   - Crie um projeto e ative a API Google Classroom.
   - Baixe o arquivo de credenciais (`credentials.json`) e coloque-o na raiz do projeto.

2. **Autenticação Inicial**:
   - Na primeira execução, será solicitado que você autorize o acesso ao Google Classroom.
   - Após a autenticação, será gerado o arquivo `token.json`.

---

## Como Executar

### 1. Executar o servidor Flask

Inicie a API para criar atividades:

```bash
python integracao.py
```

A API estará disponível em `http://localhost:8080`.

### 2. Listar Cursos Disponíveis

Execute o script `listarCursos.py` para listar os cursos disponíveis:

```bash
python listarCursos.py
```

---

## Endpoints da API

### Verificar API
- **Método**: `GET`
- **Rota**: `/`
- **Descrição**: Retorna uma mensagem confirmando que a API está ativa.

### Criar Atividade
- **Método**: `POST`
- **Rota**: `/criar_atividade`
- **Payload**:
  ```json
  {
    "titulo": "Título da Atividade",
    "descricao": "Descrição da Atividade",
    "alternativas": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D", "Alternativa E"],
    "resposta_correta": "Alternativa A",
    "id_curso": "ID do Curso"
  }
  ```
- **Resposta**:
  ```json
  {
    "mensagem": "Atividade criada com sucesso!",
    "id": "ID da Atividade"
  }
  ```

---

## Estrutura de Diretórios

```
├── credentials.json
├── token.json
├── integracao.py
├── listarCursos.py
└── README.md
```

---

## Contribuições

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias.

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
