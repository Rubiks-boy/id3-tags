from scrape_album_list import get_album_info
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
import glob

OAUTH = ""

spotify_album_ids = []


albums = []

for album_id in spotify_album_ids:
    album_id = album_id[14:]
    albums.append(get_album_info(album_id, OAUTH)["tracks"])

filez = glob.glob("../intake/**/*.mp3", recursive=True)


print(f"Intaking {len(filez)} mp3 files")

modified = 0
for f in filez:
    mp3file = MP3(f, ID3=EasyID3)

    if mp3file == {}:
        continue

    song_title = mp3file["title"][0]

    # for each file, find the metadata pulled from spotify
    # and update the track num accordingly
    for album in albums:
        if song_title in album:
            correct_track_num = str(album[song_title]["track"])

            if mp3file["tracknumber"][0] != correct_track_num:
                print(f"{correct_track_num} {song_title}")
                mp3file["tracknumber"] = [correct_track_num]
                mp3file.save()
                modified = modified + 1
            continue


print(f"{modified} songs changed")
