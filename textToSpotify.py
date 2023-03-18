#   This program will store the song title and artist of every song from a spotify playlist
#   in a JSON object.
#
#   Spotipy is a lightweight Python library for the Spotify Web API. With Spotipy you get full
#   access to all of the music data provided by the Spotify platform.
#
#   Spotipy supports two authorization flows:
#       - The Authorization Code flow: This method is suitable for long-running applications which
#         the user logs into once. It provides an access token that can be refreshed.
#               NOTE: Requires you to add a redirect URI to your application at My Dashboard.
#                     See Redirect URI for more details.
#
#        - The Client Credentials flow: The method makes it possible to authenticate your requests
#          to the Spotify Web API and to obtain a higher rate limit than you would with the
#         Authorization Code flow.
#
#   The Authorization Code flow is more appropiate for this application since we want to get information
#   about the user's private playlists and the Cliend Credentials flow allows access only to endpoints
#   that do not access user information.
#
#   classspotipy.oauth2.SpotifyOAuth(client_id=None, client_secret=None, redirect_uri=None, state=None,
#                                    scope=None, cache_path=None, username=None, proxies=None, show_dialog=False,
#                                    requests_session=True, requests_timeout=None, open_browser=True, cache_handler=None)
#
#   user_playlist(user, playlist_id=None, fields=None, market=None)

import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-private"

auth_manager = SpotifyOAuth( client_id = '4bcd5f860bd34ec3be146b636275b18e',
                             client_secret = '1c439a19f94542feaad8b4227a7c4aaf',
                             redirect_uri = 'http://localhost:8080',
                             scope = 'playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public')

sp = spotipy.Spotify(auth_manager=auth_manager)

user = sp.me()
count = 0
failed = 0

fp = open('songs.txt', 'r')
total = len(fp.readlines())
fp.close()

def addToPlaylist(playlist_name):
    playlists = sp.user_playlists(user['id'], limit = None)
    playlist_names = [playlist['name'] for playlist in playlists['items']]

    if playlist_name not in playlist_names:
        print('There is no playlist with the name "' + playlist_name + '". Please input an existing playlist name.')
        return False

    playlist_id = [playlist['id'] for playlist in playlists['items'] if playlist['name'] == playlist_name][0]

    fp_songs = open('songs.txt', 'r')
    fp_failed = open('failed.txt', 'w')

    global count
    global failed

    for line in fp_songs:
        search_result = sp.search(q = line, type = 'track', limit = 1, offset = 0)
        try:
            uri = search_result['tracks']['items'][0]['uri']
            sp.playlist_add_items(playlist_id,[uri])

            count += 1
            print('Added ' + str(count) + ' of ' + str(total) + ' songs.')
        except:
            print('Failed to find any results similar to: "' + line.strip() + '"')
            fp_failed.write(line)
            failed += 1

    fp_songs.close()
    fp_failed.close()

    return True


print('Master, what would you like to do?')
print('     1. Add the songs to an existing playlist.')
print('     2. Create a new playlist.')

caseToken = None
while caseToken not in ["1", "2"]:
    caseToken = input("Choose <1> or <2>: ")

if caseToken == "1":
    playlist_name = input("What is the name of your Spotify playlist?\nName: ")
    while addToPlaylist(playlist_name) is False:
        playlist_name = input("What is the name of your Spotify playlist?\nName: ")
    
    print( str(count) + '/' + str(total) + ' songs have been added to "' + playlist_name + '".')
    if failed > 0:
        print('We failed to add '+ str(failed) +'/' + str(total) +' songs to the playlist "' + playlist_name + '".')
        print('Please check the failed.txt file to see which songs failed.')


if caseToken == "2":
    playlist_name = input("How do you want to name your Spotify playlist?\nName: ")
    
    playlist_type = None
    while playlist_type not in ["y", "n"]: 
        playlist_type = input('Do you want "' + playlist_name + '" to be public? (y/n): ')

    public = False
    if playlist_type == "y":
        public = True

    sp.user_playlist_create(user['id'], playlist_name, public = public)

    addToPlaylist(playlist_name)
    print( str(count) + '/' + str(total) + ' songs have been added to "' + playlist_name + '".')
    if failed > 0:
        print('We failed to add '+ str(failed) +'/' + str(total) +' songs to the playlist "' + playlist_name + '".')
        print('Please check the failed.txt file to see which songs failed.')
