import requests

def buscar_dados(token):
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


    return list(artista_dict.values())
   