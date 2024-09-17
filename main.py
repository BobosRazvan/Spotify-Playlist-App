from bs4 import BeautifulSoup
import requests

redirect_uri = "http://localhost:8888/callback"
scope = "playlist-modify-private"

Client_ID=""
Client_secret = ""

date = input("Which year you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
response.raise_for_status()

yc_web_page = response.text

soup = BeautifulSoup(yc_web_page,"html.parser")

titles = soup.select('li ul li h3')

# for title in titles:
#     # print(title.getText().strip())


import spotipy
from spotipy.oauth2 import SpotifyOAuth

birdy_uri = ''
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID, client_secret=Client_secret, redirect_uri=redirect_uri, scope=scope))



user_id = spotify.me()['id']
playlist_name = f"{date} Billboard 100"
playlist = spotify.user_playlist_create(user_id, playlist_name, public=False)
playlist_id = playlist['id']

song_uris = []
for title in titles:
    song_name = title.getText().strip()
    result = spotify.search(q=f'track:{song_name}', type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"Song: {song_name} not found on Spotify")

spotify.playlist_add_items(playlist_id, song_uris)
