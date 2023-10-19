from bs4 import *
from spotipy import *
import requests



CLIENT_ID = '...'
CLIENT_SECRET = '...'
APP_REDIRECT_URI = 'http://example.com'

date = input('Type the data in format YYYY-MM-DD:\n')
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)



sp = Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                       scope="playlist-modify-private",
                                        client_secret=CLIENT_SECRET,
                                        redirect_uri=APP_REDIRECT_URI,
                                        show_dialog=True,
                                        cache_path="token.txt",
                                        username='...'))


user_id = sp.current_user()["id"]


soup = BeautifulSoup(response.text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)