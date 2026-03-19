import os
import requests
import logging
from requests.auth import HTTPBasicAuth
from flask import session

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def buscar_dados(token):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50"

    headers = {"Authorization": f"Bearer {token}"}    

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 401:
        logging.info("Token expirado, tentando renovar...")

        new_token = refresh_access_token()

        if not new_token:
            logging.error("Falha ao renovar o token.")
            return None
    
        headers['Authorization'] = f"Bearer {new_token}"
        response = requests.get(url, headers=headers)   

    if response.status_code != 200:
        logging.error(f"Erro ao buscar dados: {response.status_code} - {response.text}")
        return None

    tracks = response.json().get('items', [])
    
    artista_dict = {}
    for t in tracks:
        artists = t.get('artists', [])
        main_artist = artists[0]['name'] if artists else "Desconhecido"

        album = t.get('album', {})
        images = album.get('images', [])

        if main_artist not in artista_dict:
            artista_dict[main_artist] = {
                'nome': main_artist,
                'fotos': images,
                'top_musicas': []
            }
        artista_dict[main_artist]['top_musicas'].append({
            'id': t['id'],
            'nome': t['name'],
            'preview_url': t.get('preview_url')  
        })


    return list(artista_dict.values())
   

def user_data(token):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        logging.error(f"Erro ao buscar dados do usuário: {response.status_code} - {response.text}")
        return None 
    
    return response.json()

def refresh_access_token():
    refresh_token = session.get('refresh_token')

    if not refresh_token:
        return None
    
    if not CLIENT_ID or not CLIENT_SECRET:
        raise Exception("CLIENT_ID ou CLIENT_SECRET não configurados.")

    try:
        res = requests.post(
            "https://accounts.spotify.com/api/token",
            data={'grant_type': 'refresh_token', 'refresh_token': refresh_token},
            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), timeout=10
        )

        if res.status_code != 200:
            return None
        
        new_token = res.json().get('access_token')

        if new_token:
            session['access_token'] = new_token

        return new_token

    except Exception as e:
        logging.error(f"Erro ao renovar o token: {str(e)}")
        return None
