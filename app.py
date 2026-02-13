import io
import base64
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import time
from cs50 import SQL
import black
import os
from contextlib import redirect_stdout
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask_session import Session
from openai import OpenAI
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
load_dotenv()
db = SQL("sqlite:///data.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/ia", methods=["POST"])
@login_required
def ia():
    try:
        data = request.get_json()
        code = data.get("code", "")
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return jsonify({"output": "Erro: GROQ_API_KEY nao configurada."}), 400
        client = OpenAI(api_key=api_key,
                        base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Voce e um assistente util e especialista em Python. Leia o codigo e diga como melhorar, incluindo notacao Big O.",
                },
                {"role": "user", "content": code},
            ],
        )
        output = response.choices[0].message.content
    except Exception as e:
        output = f"Erro: {e}"
    return jsonify({"output": output})


@app.route("/compare", methods=["POST"])
@login_required
def compare_codes():
    try:
        fig, ax = plt.subplots()
        output = db.execute(
            "SELECT * FROM tempo WHERE user_id = ?", session["user_id"])
        tempos = []
        ids = []
        for valor in output:
            tempos.append(valor["tempo"])
            ids.append(valor["id"])

        ax.bar(ids, tempos, color='red')
        ax.set_ylabel('Tempo (s)')
        ax.set_xlabel('Id da tentativa')
        ax.set_title('Tempo de Execução')

        # Salvar em memória como PNG
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)

        output = f"<img src='data:image/png;base64,{img_base64}' style='max-width: 100%;'>"
    except Exception as e:
        output = f"Erro: {e}"

    return jsonify({"output": output})


@app.route("/save", methods=["POST"])
@login_required
def save_code():
    try:
        data = request.get_json()
        tempo = data.get("tempo", "")
        output = db.execute("INSERT INTO tempo (user_id, tempo) VALUES (?, ?)",
                            session["user_id"], tempo)
    except Exception as e:
        output = f"Erro: {e}"
    return jsonify({"output": output})


@app.route("/run", methods=["POST"])
@login_required
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    start = time.time()
    try:
        local_vars = {}
        formatted = black.format_str(code, mode=black.FileMode())
        stdout_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer):
            exec(formatted, {}, local_vars)
        printed = stdout_buffer.getvalue().strip()
        vars_output = str(local_vars)
        if printed:
            output = f"Saida:\n{printed}\n\nVariaveis:\n{vars_output}"
        else:
            output = f"Variaveis:\n{vars_output}"
    except Exception as e:
        output = f"Erro: {e}"
    end = time.time()
    return jsonify({"output": output, "execution_time": end - start})


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        try:
            hash = generate_password_hash(request.form.get("password"))
            result = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                request.form.get("username"),
                hash,
            )
            return redirect("/login")
        except ValueError:
            return apology("already exists an user with this name", 400)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    db.execute("DELETE FROM tempo WHERE user_id = ?", session["user_id"])
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
