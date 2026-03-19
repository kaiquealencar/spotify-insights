import os
import requests
import sys
import logging
from flask import Flask, render_template, redirect, request, session
from requests.auth import HTTPBasicAuth
from services.spotify_service import buscar_dados, user_data

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    scope = "user-top-read user-read-private user-read-email"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "show_dialog": "true"
    }
    from urllib.parse import urlencode
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')

    if not code:
        return "Erro: Código de autorização não encontrado.", 400

    try:
        res = requests.post("https://accounts.spotify.com/api/token", 
        data={'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI},
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))

        if res.status_code != 200:
            return f"Erro ao obter token de acesso: {res.text}", 400
                
        data = res.json()

        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')

        if not access_token:
            return "Erro: Token de acesso não encontrado.", 400
        
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token


        return redirect("/dashboard")
    
    except Exception as e:
        logging.error(f"Erro ao obter token de acesso: {str(e)}")
        return "Erro ao obter token de acesso.", 500

@app.route('/dashboard')
def dashboard():
    token = session.get('access_token')

    if not token:
        return redirect('/login')
    
    try:
        artistas = buscar_dados(token)
        user_info = user_data(token)
        nome_usuario = user_info.get('display_name', 'Usuário') if user_info else 'Usuário'
        foto_usuario = user_info.get('images', [{}])[0].get('url', '') if user_info else ''
        perfil_url = user_info.get('external_urls', {}).get('spotify', '#') if user_info else '#'

        return render_template("dashboard.html", nome=nome_usuario, foto=foto_usuario, perfil_url=perfil_url, lista_v2=artistas)
    except Exception as e:
        return f"Erro ao buscar dados do Spotify.{str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True, port=9000)