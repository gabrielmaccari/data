# DATA
#### Video Demo: https://www.youtube.com/watch?v=ayojLS9MwyY

## Project

Flask application for studying Python. Main features:

- User registration and login
- Execution of Python code in the browser with execution time display
- Code analysis via Groq (OpenAI API compatible)
- Graph with historical times per user

## Requirements

- Python 3.10+
- SQLite
- Dependencies listed in requirements.txt

## Configuration

Create a .env file in the project root with your key:

```env GROQ_API_KEY=put_your_key_here
```

The .env file is ignored in Git for security reasons.

## How to run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

```

Access http://127.0.0.1:5000

## Quick structure

- app.py: routes and main logic
- helpers.py: login_required and error page
- templates/: HTML
- static/: CSS and images
- data.db: SQLite database

## Notes

- The /run route executes the submitted code; use only in a local environment.

- The graph uses data from the time table in SQLite.
