import requests

URL = "https://api.spotify.com/v1/albums/%s/tracks"


def get_song_order(album_id, oauth_token):
    resp = requests.get(
        URL % album_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        },
    )

    album = resp.json()["items"]

    album_info = {}

    for song in album:
        song_name = song["name"]
        artists = [artist["name"] for artist in song["artists"]]
        disc_number = song["disc_number"]
        track_number = song["track_number"]

        album_info[song_name] = {
            "artists": artists,
            "disc": disc_number,
            "track": track_number,
        }

    return album_info