# Some songs don't have the "albumartist" metadata tag.
# Based on the artist metadata and also where the file is
# (ex. iTunes media folder usually stores artist name in the directory)
# this script will try to fill in the albumartist tag.
# if it can't, it'll output the songs it doesn't know what to do with.
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
import glob


# extract the file names (including folders)
# for the mp3s in the album
filez = glob.glob("intake/**/*.mp3", recursive=True)

print(f"Intaking {len(filez)} mp3 files")

modified = 0
for f in filez:
    mp3file = MP3(f, ID3=EasyID3)

    # Mp3 without metadata
    # ex. this happens if you create the mp3 yourself
    if mp3file == {}:
        print(f"{f}: No metadata :(")
        continue

    if "albumartist" not in mp3file:
        # itunes sometimes stores album artist within the directory
        # try to use this to predict what the artist should be
        predicted_artist = f.split("/")[-3]

        artist = mp3file["artist"]

        if artist[0] == predicted_artist:
            mp3file["albumartist"] = artist
            mp3file.save()
            modified += 1
        else:
            print(
                f"Don't know what to do with: {mp3file['artist'][0]}\t{predicted_artist}\t{mp3file['title'][0]}"
            )

print(f"{modified} songs changed")
