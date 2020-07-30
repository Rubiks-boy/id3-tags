# Scripts for Managing iTunes library
## Why?
Old iPods are a ton of fun! However, managing iTunes media libraries is a challenge, and I'm not a fan of manually pressing get info on every song.

On some older iPods, there's also some [weird behavior](https://discussions.apple.com/thread/2254718) surrounding cover flow displaying the same albums twice. Also, songs with multiple artists, say A and B, will have an artist listed as "A; B", which is viewed as distinct from artist "A" and artist "B", cluttering the artists page.

These scripts try to address these types of issues.
## Using the scripts
Git clone and `pip install -r pip-requirements.txt`.

Copy your iTunes library's music folder to "./intake/music", and run the applicable script. See documentation at the top of each script to see what each script does. When running, the output can be long, depending on the size of your music library; you might want to save the output to a file.

I _strongly_ recommend you create a backup of your iTunes folder! It's relatively difficult to go back and undo some of the changes that were made.