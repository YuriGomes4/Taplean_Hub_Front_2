from flask import Flask, redirect, render_template, request, url_for
import functools
from flask_cors import CORS
import requests
app = Flask(__name__)

CORS(app)

def token_required(route_func):
    @functools.wraps(route_func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if token:
            response = requests.get('http://localhost:5000/api/auth/verify', headers={'x-access-token': token})
            if response.status_code == 200:
                return route_func(*args, **kwargs)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/')
@token_required
def index():
    return redirect(url_for('graficos'))
	
@app.route("/login")
#@token_required
def login():
    pagina = "login"
    return render_template("login.html", pagina=pagina)

@app.route("/graficos")
@token_required
def graficos():
    pagina = "graficos"
    return render_template("principais/graficos.html", pagina=pagina)

@app.route("/produtos")
@token_required
def produtos():
    pagina = "produtos"
    return render_template("principais/produtos.html", pagina=pagina)

@app.route("/anuncios")
@token_required
def anuncios():
    pagina = "anuncios"
    return render_template("principais/anuncios.html", pagina=pagina)

@app.route("/analise_mercado")
@token_required
def analise_mercado():
    pagina = "analise_mercado"
    return render_template("principais/analise_mercado.html", pagina=pagina)

@app.route("/conta")
@token_required
def conta():
    pagina = "conta"
    return render_template("principais/conta.html", pagina=pagina)

@app.route("/administracao")
@token_required
def administracao():
    pagina = "administracao"
    return render_template("principais/administracao.html", pagina=pagina)

app.static_folder = 'templates/assets'

if __name__ == "__main__":
    app.run(port=5050, debug=True)
