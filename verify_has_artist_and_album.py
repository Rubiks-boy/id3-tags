# Verifies that songs in the iTunes library have exactly one artist,
# that the artist is the same as the album artist,
# and that there is an album name
# outputs any songs that don't conform to this
# this file doesn't modify any files.
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
import glob


# extract the file names (including folders)
# for the mp3s in the album
filez = glob.glob("intake/**/*.mp3", recursive=True)

print(f"Intaking {len(filez)} mp3 files")

for f in filez:
    mp3file = MP3(f, ID3=EasyID3)

    # Mp3 without metadata
    # ex. this happens if you create the mp3 yourself
    if mp3file == {}:
        print(f"{f}: No metadata :(")
        continue

    if "artist" not in mp3file:
        print(f"No artist: {mp3file['title'][0]}")
    elif ";" in mp3file["artist"][0]:
        print(f"Multiple artists: {mp3file['title'][0]}")
    elif mp3file["artist"] != mp3file["albumartist"]:
        print(
            f"Diff artist: {mp3file['title'][0]} {mp3file['artist'][0]} {mp3file['albumartist'][0]}"
        )
    if "album" not in mp3file:
        print(f"No album: {mp3file['title'][0]}")
