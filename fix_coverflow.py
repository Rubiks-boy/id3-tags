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

for f in filez:
    mp3file = MP3(f, ID3=EasyID3)

    if mp3file == {}:
        print(f"{f}: No metadata :(")
        continue

    try:
        # grab artist, album artist, title metadata
        title = mp3file["title"]
        assert len(title) == 1
        title = title[0]
        if "artist" not in mp3file:
            print(f"{f} {title}:  no artist")
            continue
        artist = mp3file["artist"]
        assert len(artist) == 1
        artist = artist[0]

        # artists are stored like: A; B; C
        # separate into list
        curr_artists = artist.split("; ")
        # sanity check that the splitting worked
        # goal: catch weird issues with "Foo" and "Foo " listing as two separate artists
        for a in curr_artists:
            assert a.find(";") == -1
            assert a[0] != " "
            assert a[-1] != " "

        if "albumartist" not in mp3file:
            # try to guess at what the album artist is
            # based on the iTunes file path
            fpath = f.split("/")

            albumartist = fpath[-3]

            # We cant trust this guess, so verify it against the artists list
            if albumartist not in curr_artists:
                print(f"{f} {title}:  no albumartist")
                continue
        else:
            # Normal case of there being an album artist to go off of
            albumartist = mp3file["albumartist"]
            assert len(albumartist) == 1
            albumartist = albumartist[0]

            if albumartist not in curr_artists:
                print(f"{f} {title}:  albumartist not in artists")
                continue

        # see if this is a song we need to worry about
        if len(curr_artists) > 1 and "feat" not in title:
            # feat artists = those that aren't the album artist
            feat_artists = list(curr_artists)
            feat_artists.remove(albumartist)

            # format new title
            new_title = f"{title} {feat_str(feat_artists)}"

            # save this new metadata
            mp3file["artist"] = albumartist
            mp3file["title"] = new_title
            mp3file.save()
            print(f"\t{new_title},{albumartist},{title},{curr_artists}")
        elif len(curr_artists) > 1 and "feat" in title:
            # in the event a song has "feat. A and B" and lists A and B as artists,
            # try to remove A and B from the artist fields and only keep the album artist
            # feat artists = those that aren't the album artist
            feat_artists = list(curr_artists)
            feat_artists.remove(albumartist)

            assert albumartist not in title

            all_feats_in_title = True
            for artist in feat_artists:
                if artist not in title:
                    all_feats_in_title = False

            if all_feats_in_title:
                mp3file["artist"] = albumartist
                mp3file.save()
                print(f"\t{title},{albumartist},{title},{curr_artists}")
            else:
                print(f"{f} {title}: feat field artists don't match artists in tags")
    except Exception as e:
        print(f)
        continue
