# DATA
#### Video Demo: https://www.youtube.com/watch?v=ayojLS9MwyY

## Projeto

Aplicacao Flask para estudar Python. Funcionalidades principais:
- cadastro e login de usuarios
- execucao de codigo Python no navegador com tempo de execucao
- analise de codigo via Groq (API OpenAI compativel)
- grafico com historico de tempos por usuario

## Requisitos

- Python 3.10+
- SQLite
- Dependencias listadas em requirements.txt

## Configuracao

Crie um arquivo .env na raiz do projeto com sua chave:

```env
GROQ_API_KEY=coloque_sua_chave_aqui
```

O arquivo .env esta ignorado no Git por seguranca.

## Como rodar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000

## Estrutura rapida

- app.py: rotas e logica principal
- helpers.py: login_required e pagina de erro
- templates/: HTML
- static/: CSS e imagens
- data.db: banco SQLite

## Notas

- A rota /run executa o codigo enviado; use apenas em ambiente local.
- O grafico usa dados da tabela tempo no SQLite.
