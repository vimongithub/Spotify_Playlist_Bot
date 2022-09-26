import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_ID = "91db4f87cf6b44deb7e5fcfc6e17f412"
SPOTIFY_SECRET_CODE = "557d3869099a4205a0e94f7e9a0a2928"
REDIRECT_URI = "https://example.com/callback"
URL = "https://www.billboard.com/charts/hot-100/"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET_CODE,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

travel_date = input("which year you want to travel ? Enter the date in yyyy-mm-dd format:")

billboard_response = requests.get(f"{URL}{travel_date}/")
billboard_html = billboard_response.text

soup = BeautifulSoup(billboard_html, "html.parser")
song_titles = soup.find_all(name="h3", id="title-of-a-story")

songs_list = [title.getText().strip() for title in song_titles]
songs_list = list(dict.fromkeys(songs_list))

song_list_100 = [songs_list[number] for number in range(6, 106)]
song_uris = []
year = travel_date.split("-")[0]

for song in song_list_100:
    result = sp.search(q=f"track{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=user_id, name=f"{travel_date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
