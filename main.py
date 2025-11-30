import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date = input("Which year do you want to travel to? Type the date in this format, YYYY-MM-DD:\n")
header = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
billboard_url = "https://www.billboard.com/charts/hot-100/"+date
response = requests.get(url=billboard_url, headers=header)
top_song = response.text

soup = BeautifulSoup(top_song, "html.parser")
song_data = soup.select("li ul li h3")
song_title = [song.getText().strip() for song in song_data]

# Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id= os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

play_list = sp.user_playlist_create(user = user_id, name=f"{date} Billboard Hot 100", public=False)
#print(play_list)
sp.playlist_add_items(playlist_id=play_list["id"], items=song_uris)


