import os, requests, sys
from flask import Flask, render_template, redirect, request
from requests.auth import HTTPBasicAuth

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
    res = requests.post("https://accounts.spotify.com/api/token", 
        data={'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI},
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    
    token = res.json().get('access_token')
    
    user_info = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {token}"}).json()
    print(f"\n[CHECK] Spotify diz que você é: {user_info.get('email')}")

    artistas = buscar_dados_v2(token)
    return render_template("dashboard.html", lista_v2=artistas)


def buscar_dados_v2(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    res = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50", headers=headers)
    tracks = res.json().get('items', [])
    
    artista_dict = {}
    for t in tracks:
        main_artist = t['artists'][0]['name']
        if main_artist not in artista_dict:
            artista_dict[main_artist] = {
                'nome': main_artist,
                'fotos': t['album']['images'],  
                'top_musicas': []
            }
        artista_dict[main_artist]['top_musicas'].append({
            'id': t['id'],
            'nome': t['name'],
            'preview_url': t.get('preview_url')  
        })
    
    return [
        {
            'nome': a['nome'],
            'fotos': a['fotos'],
            'top_musicas': a['top_musicas']
        }
        for a in artista_dict.values()
    ]


if __name__ == '__main__':
    app.run(debug=True, port=9000)