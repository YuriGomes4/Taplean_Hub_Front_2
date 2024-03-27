from datetime import datetime, timedelta
import difflib
import json
import uuid
from flask import Flask, redirect, render_template, request, url_for, session
import functools
from flask_cors import CORS
import requests

import services
import pandas as pd
import plotly.express as px

app = Flask(__name__)

CORS(app)

base_url = services.config.get('url_base')

def token_required(route_func):
    @functools.wraps(route_func)
    def wrapper(*args, **kwargs):
        #token = request.cookies.get('token')
        #if token:
        #    response = requests.get(f'{base_url}/api/auth/verify', headers={'x-access-token': token})
        #    if response.status_code == 200:
        #        return route_func(*args, **kwargs)
        #    else:
        #        return redirect(url_for('login'))
        #else:
        #    return redirect(url_for('login'))
        
        if 'uid' in session.keys():
            session_id = str(session['uid'])
            remote_adr = str(request.remote_addr)

            response = requests.get(f'{base_url}/api/auth/verify', headers={'x-session-id': session_id, 'x-remote-adr': remote_adr})
            if response.status_code == 200:
                return route_func(session_id, remote_adr, *args, **kwargs)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        
    return wrapper

@app.route('/')
@token_required
def index(session_id, remote_adr):
    return redirect(url_for('graficos'))
	
@app.route("/login")
#@token_required
def login():

    if 'uid' not in session.keys():
        session['uid'] = uuid.uuid4()
        session_id = str(session['uid'])
    else:
        session_id = str(session['uid'])

    #token = request.cookies.get('token')
    #if token:
    #    response = requests.get(f'{base_url}/api/auth/verify', headers={'x-access-token': token})
    #    if response.status_code == 200:
    #        return redirect(url_for('graficos'))
    #    else:
    #        pagina = "login"
    #        return render_template("login.html", base_url=base_url, pagina=pagina)
    #else:
    #    pagina = "login"
    #    return render_template("login.html", base_url=base_url, pagina=pagina)
        
    response = requests.get(f'{base_url}/api/auth/verify', headers={'x-session-id': session_id, 'x-remote-adr': request.remote_addr})
    if response.status_code == 200:
        return redirect(url_for('graficos'))
    else:
        pagina = "login"
        return render_template("login.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=request.remote_addr)

@app.route("/graficos")
@token_required
def graficos(session_id, remote_adr):
    pagina = "graficos"

    estados_brasil = {
        "Brasil": "BR",
        "Acre": "AC",
        "Alagoas": "AL",
        "Amapá": "AP",
        "Amazonas": "AM",
        "Bahia": "BA",
        "Ceará": "CE",
        "Distrito Federal": "DF",
        "Espírito Santo": "ES",
        "Goiás": "GO",
        "Maranhão": "MA",
        "Mato Grosso": "MT",
        "Mato Grosso do Sul": "MS",
        "Minas Gerais": "MG",
        "Pará": "PA",
        "Paraíba": "PB",
        "Paraná": "PR",
        "Pernambuco": "PE",
        "Piauí": "PI",
        "Rio de Janeiro": "RJ",
        "Rio Grande do Norte": "RN",
        "Rio Grande do Sul": "RS",
        "Rondônia": "RO",
        "Roraima": "RR",
        "Santa Catarina": "SC",
        "São Paulo": "SP",
        "Sergipe": "SE",
        "Tocantins": "TO"
    }

    return render_template("principais/graficos.html", base_url=base_url, pagina=pagina, estados_brasil=estados_brasil, session_id=session_id, remote_adr=remote_adr)

@app.route("/produtos")
@token_required
def produtos(session_id, remote_adr):
    pagina = "produtos"
    return render_template("principais/produtos.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=remote_adr)

@app.route("/produto/<string:mlb>")
@token_required
def produto(session_id, remote_adr, mlb):
    pagina = "produtos"
    return render_template("principais/produto.html", base_url=base_url, pagina=pagina, mlb=mlb, session_id=session_id, remote_adr=remote_adr)

@app.route("/anuncios")
@token_required
def anuncios(session_id, remote_adr):
    pagina = "anuncios"
    return render_template("principais/anuncios.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=remote_adr)

@app.route("/anuncios/pesquisar")
@token_required
def anuncios_pesquisar(session_id, remote_adr):
    pagina = "anuncios"
    return render_template("principais/anuncios_pesquisar.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=remote_adr)

@app.route("/analise_mercado")
@token_required
def analise_mercado(session_id, remote_adr):
    pagina = "analise_mercado"
    return render_template("principais/analise_mercado.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=remote_adr)

@app.route("/analise_mercado/nova")
@token_required
def nova_analise_mercado(session_id, remote_adr):
    pagina = "analise_mercado"
    return render_template("principais/nova_analise_mercado.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=remote_adr)

@app.route("/analise_mercado/<string:id_pesquisa>")
@token_required
def ver_analise_mercado(session_id, remote_adr, id_pesquisa):
    pagina = "analise_mercado"
    return render_template("principais/ver_analise_mercado.html", base_url=base_url, pagina=pagina, id_pesquisa=id_pesquisa, session_id=session_id, remote_adr=remote_adr)

@app.route("/analise_mercado/<string:id_pesquisa>/addprodutos")
@token_required
def analise_mercado_addprodutos(session_id, remote_adr, id_pesquisa):
    pagina = "analise_mercado"
    return render_template("principais/analise_mercado_addprodutos.html", base_url=base_url, pagina=pagina, id_pesquisa=id_pesquisa, session_id=session_id, remote_adr=remote_adr)

@app.route("/conta")
@token_required
def conta(session_id, remote_adr):
    pagina = "conta"
    return render_template("principais/conta.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=remote_adr)

#http://173.249.39.42:5050/conta/novo_vendedor/cb6e401c-f62c-4aef-9562-dc3ed60708a9

@app.route("/conta/novo_vendedor/<string:public_id>")
@token_required
def novo_vendedor(session_id, remote_adr, public_id):
    pagina = "conta"
    return render_template("principais/novo_vendedor.html", base_url=base_url, pagina=pagina, public_id=public_id, session_id=session_id, remote_adr=remote_adr)

@app.route("/administracao")
@token_required
def administracao(session_id, remote_adr):
    pagina = "administracao"
    return render_template("principais/administracao.html", base_url=base_url, pagina=pagina, session_id=session_id, remote_adr=remote_adr)

@app.route("/criar_conta")
def criar_conta(session_id, remote_adr):
    email_id = request.args.get('ver')
    code = request.args.get('c')
    #pagina = "criar_conta"
    return render_template("criar_conta.html", base_url=base_url, ver=email_id, c=code)

@app.route("/verificar_email")
def verificar_email():
    #pagina = "criar_conta"
    return render_template("verif_email.html", base_url=base_url)#pagina=pagina

@app.route("/validar_email")
def validar_email():
    email_id = request.args.get('ver')
    #pagina = "validar_email"
    return render_template("validar_email.html", base_url=base_url, ver=email_id)

app.static_folder = 'templates/assets'
app.config['SECRET_KEY'] = 'um_dia_o_sol_vai_brilhar'

if __name__ == "__main__":
    app.run(port=5050, debug=True, host="0.0.0.0")
