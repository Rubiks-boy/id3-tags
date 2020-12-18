import requests

URL = "https://api.spotify.com/v1/albums/%s"


def get_album_info(album_id, oauth_token):
    resp = requests.get(
        URL % album_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        },
    )

    album = resp.json()["tracks"]["items"]

    album_tracks = {}

    for song in album:
        song_name = song["name"]
        artists = [artist["name"] for artist in song["artists"]]
        disc_number = song["disc_number"]
        track_number = song["track_number"]

        album_tracks[song_name] = {
            "artists": artists,
            "disc": disc_number,
            "track": track_number,
        }

    candidate_artists = list(album_tracks.values())[0]["artists"]
    for song in album_tracks.values():
        if len(candidate_artists) == 1:
            break
        candidate_artists = [
            candidate for candidate in candidate_artists if candidate in song["artists"]
        ]

    if len(candidate_artists) > 1:
        raise Exception("More than one album artist")

    return {"album_artist": candidate_artists[0], "tracks": album_tracks}
