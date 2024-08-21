# LLM SaaS API

Este é um projeto Flask que utiliza SQLAlchemy para gerenciamento de banco de dados e Bcrypt para criptografia de senhas. O projeto inclui uma configuração para uma API OpenAI Compatible que interage com a API da Ollama, possibilitando a utilização de qualquer modelo disponível no site da Ollama.

## Diagrama de Classes

```mermaid
classDiagram
    class User {
        +int id
        +str username
        +str password_hash
        +str api_key
        +int tokens_used
    }

    class Config {
        +str SQLALCHEMY_DATABASE_URI
        +bool SQLALCHEMY_TRACK_MODIFICATIONS
        +str OLLAMA_BASE_URL
    }

    class APIError {
        +str message
        +int status_code
    }

    class auth {
        +register()
        +login()
    }

    class llm {
        +list_models()
        +chat_completions()
        +completions()
    }

    class user {
        +get_usage()
    }

    class TokenCounter {
        +get_tokenizer()
        +count_tokens()
        +update_token_usage()
    }

    class OllamaService {
        +get_models()
        +generate_chat_completion()
        +generate_completion()
    }

    APIError ..> User : uses
    auth ..> User : interacts with
    llm ..> OllamaService : uses
    llm ..> TokenCounter : uses
    user ..> User : uses
    TokenCounter ..> User : updates
    OllamaService ..> Config : uses
```

## Configuração do Ambiente Virtual

Para criar e ativar um ambiente virtual Python, siga estes passos:

1. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   ```

2. **Ative o ambiente virtual:**

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No macOS e Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências:**

   Com o ambiente virtual ativado, instale as dependências listadas em `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. **Configuração do Ambiente**

   Crie um arquivo `.env` na raiz do projeto e adicione a seguinte variável de ambiente:

   ```
   OLLAMA_BASE_URL=http://localhost:11434
   ```

   Este URL é utilizado para se conectar à API da Ollama.

2. **Banco de Dados**

   O projeto utiliza SQLite para armazenamento de dados. O banco de dados será criado automaticamente na primeira execução do aplicativo.

## Estrutura do Projeto

- `app.py`: Configura a aplicação Flask e registra os blueprints das rotas.
- `config.py`: Contém a configuração do aplicativo, incluindo a URL do banco de dados e a URL base da Ollama.
- `models.py`: Define o modelo `User` para o banco de dados.
- `utils/extensions.py`: Contém a inicialização do `db` e `bcrypt`.
- `utils/decorators.py`: Contém decoradores para validação de API key e manipulação de erros.
- `routes/`: Diretório contendo os blueprints para as rotas `auth`, `llm` e `user`.
- `services/`: Diretório contendo os serviços para interação com a API da Ollama e contagem de tokens.

## Rotas

### Auth

- **`POST /register`**: Registra um novo usuário. Exige `username` e `password` no corpo da requisição. Retorna um `api_key` para o usuário registrado.
- **`POST /login`**: Realiza login de um usuário existente. Exige `username` e `password` no corpo da requisição. Retorna o `api_key` do usuário se as credenciais forem válidas.

### LLM

- **`GET /v1/models`**: Lista todos os modelos disponíveis. Exige uma chave API válida no cabeçalho da requisição.
- **`POST /v1/chat/completions`**: Gera uma resposta para uma conversa com base nos `messages` e no `model` fornecido. Suporta streaming de respostas.
- **`POST /v1/completions`**: Gera uma conclusão para um prompt de texto com base no `model` fornecido.

### User

- **`GET /user/usage`**: Retorna o uso de tokens do usuário autenticado. Exige uma chave API válida no cabeçalho da requisição.

## Serviços

### `ollama_service`

- **`get_models()`**: Recupera a lista de modelos disponíveis da API da Ollama.
- **`generate_chat_completion(model, prompt, data, stream=False)`**: Gera uma resposta de chat para o modelo e prompt fornecidos. Suporta streaming de respostas.
- **`generate_completion(model, prompt, data)`**: Gera uma conclusão de texto para o modelo e prompt fornecidos.

### `token_counter`

- **`get_tokenizer(model_name)`**: Obtém o tokenizer para o modelo especificado, usando um fallback padrão.
- **`count_tokens(text, model_name)`**: Conta o número de tokens no texto fornecido usando o tokenizer do modelo.
- **`update_token_usage(user, token_count)`**: Atualiza o uso de tokens do usuário no banco de dados.

## Utilitários

### `utils/decorators`

- **`require_api_key(view_function)`**: Decorador que garante que a requisição contenha uma chave API válida. Se a chave estiver ausente ou inválida, retorna um erro 401.

### `utils/extensions`

- **`db`**: Instância do SQLAlchemy para gerenciamento do banco de dados.
- **`bcrypt`**: Instância do Bcrypt para criptografia de senhas.

## Executando o Projeto

Para iniciar o servidor Flask, execute o seguinte comando:

```bash
python app.py
```

O aplicativo será iniciado em modo de desenvolvimento e estará disponível em `http://127.0.0.1:5000`.

## Estrutura do Banco de Dados

O modelo de dados é definido em `models.py` e inclui a tabela `User` com os seguintes campos:

- `id`: Identificador único do usuário.
- `username`: Nome de usuário único.
- `password_hash`: Hash da senha do usuário.
- `api_key`: Chave API única para o usuário.
- `tokens_used`: Número de tokens usados pelo usuário.

## Renovação do SSL

```Bash
# Para gerar o certificado:
sudo certbot certonly --webroot --webroot-path=/home/tensordock/projects/llm_saas_api/webroot --email computecapital@gmail.com --agree-tos --no-eff-email -d api.llm.compute.capital

# Para copiar o certificado para a pasta do projeto
sudo cp /etc/letsencrypt/live/api.llm.compute.capital/fullchain.pem /home/tensordock/projects/llm_saas_api/ssl/fullchain.pem
sudo cp /etc/letsencrypt/live/api.llm.compute.capital/privkey.pem /home/tensordock/projects/llm_saas_api/ssl/privkey.pem
```

## Contribuindo

Se você deseja contribuir para este projeto, sinta-se à vontade para enviar um pull request ou abrir uma issue.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para mais informações, entre em contato com [Claudio Cassimiro](mailto:claudioletras2019@gmail.com).
