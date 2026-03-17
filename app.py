import os, requests, sys
from flask import Flask, render_template, redirect, request
from requests.auth import HTTPBasicAuth

from services.spotify_service import buscar_dados

app = Flask(__name__)

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
    
    res = requests.post("https://accounts.spotify.com/api/token", 
        data={'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI},
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    
    data = res.json()
    token = data.get('access_token')
    
    if not token:
        return "Erro: Token de acesso não encontrado.", 400
    
    user_info = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {token}"}).json()
    print(f"\n[CHECK] Spotify diz que você é: {user_info.get('email')}")

    artistas = buscar_dados(token)
    return render_template("dashboard.html", lista_v2=artistas)


if __name__ == '__main__':
    app.run(debug=True, port=9000)