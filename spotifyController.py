import spotipy
import sys
import operator
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# consts

CLIENT_ID = 'ffbf57e77cdc4d1f98b80bce63e16341'
CLIENT_SECRET = '1e612801fe654e4b956b07448461ee67'
REDIRECT_URL = 'http://localhost:8000'

songs = {}

# Function plays song on spotify - limited to first result of query
# pass in spotify username, artist name, and track name
def playSong(username, artistName, trackName):
    scope = "streaming app-remote-control user-modify-playback-state user-read-playback-state"
    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)

    sp = spotipy.Spotify(auth=token)
    results = sp.search(q='artist:' + artistName + ' track:' + trackName, type='track', limit=1)

    try:
      trackURI = results['tracks']['items'][0]['uri']
    except:
      return "Error: No results found!"

    print(sp.current_user())

    devices = sp.devices()

    try:
      deviceID = devices['devices'][0]['id']
      sp.start_playback(device_id=deviceID, uris=[trackURI])
    except:
      return "Error: Spotify must be open on one of your devices!"

    return "Now playing: " + trackName + " by " + artistName

def playNext(username):
    top_key = getNextSong()[0][0]

    popKeyValue(top_key)

    artist_title_pair = top_key.split("::")
    artist = artist_title_pair[0]
    title = artist_title_pair[1]

    playSong(username, artist, title)

def getNextSong(k = 1):
    nextsongs = []
    iterate = iter(sorted_songs)
    for i in range(k):
        nextsongs.append(next(iterate))
    return nextsongs

def popKeyValue(key):
    del songs[key]

def vote(artistName, trackName):
    key = "%s::%s" % (artistName.lower().strip(), trackName.lower().strip())

    dictionary_index = indexDictionary(key)
    if (dictionary_index):
        votes = songs[key]
        songs[key] = votes + 1
    else:
        votes = 1
        songs.update ({key : votes})

    global sorted_songs
    sorted_songs = sortDictionaryByValue()

    return "voting for %s-%s" % (artistName, trackName)

def indexDictionary(key):
    if(key in songs):
        return True
    return False

def sortDictionaryByValue():
    return sorted(songs.items(), key = lambda kv: kv[1])

def list_tracks (username):
    return str(sorted_songs)

if (__name__ == '__main__'):
    if (len(sys.argv) != 4):
        print("Usage: spotifyController.py <username> <artistName> <trackName>")
        exit()

    print(playSong(sys.argv[1], sys.argv[2], sys.argv[3]))
