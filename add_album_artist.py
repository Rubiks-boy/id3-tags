# Simple script for changing iTunes song metadata such that
# multiple artists aren't listed as separate artists in id3 tags
# and are instead put in as (feat. X and Y) in the song title
# Motivation: cover flow on classic ipods will list these as
# separate artists and albums, resulting in duplicate cover flow entries
# and a gazillion more artists.
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
import glob


def feat_str(feat_artists):
    """
    Joins the featured artists in form "(feat. A, B and C)
    No oxford comma, sorry folks
    """
    if len(feat_artists) == 1:
        return f"(feat. {feat_artists[0]})"
    else:
        last_artist = feat_artists[-1]
        other_artists = ", ".join(feat_artists[0:-1])
        return f"(feat. {other_artists} and {last_artist})"


# extract the file names (including folders)
# for the mp3s in the album
filez = glob.glob("intake/**/*.mp3", recursive=True)

print(f"Intaking {len(filez)} mp3 files")

modified = 0
for f in filez:
    mp3file = MP3(f, ID3=EasyID3)

    if mp3file == {}:
        print(f"{f}: No metadata :(")
        continue

    if "albumartist" not in mp3file:
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
