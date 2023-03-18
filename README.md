# Apple-Music-to-Spotify

This program takes the songs from an Apple Music library and saves them in a Spotify playlist.

The program is divided in 2 parts:
- Part 1: extract song title and artist from Apple Music Library to "songs.txt"
- Part 2: insert all songs from "songs.txt" to Spotify playlist

The initial plan for implementing part 1 was to connect to the Apple Music library using Apple's MusicKit API to extract the songs to a txt file, but to use the API,
I need an Apple Developer account and I do not have one at the moment. Thus, the program uses screenshots of the playlist (saved in "captures" folder) and the Pytesseract tool to extract the text from the screenshots into the "songs.txt" file.

The 2nd part of the program uses the Spotipy library for the Spotify Web API to connect to my Spotify account, create a new playlist or select an existing one, and add all songs from "songs.txt" to that playlist. The sont titles and artists that result in no match are stored in the "failed.txt" file.
