import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace with Spoify API credentials
did = "did"
c_id = "c_id"
c_secret = "c_secret"
uid = "uid"


'''
Function returns:
1 = successful
0 = no change (already in state)
-1 = critical error (currenly outside of control)
-2 = option not supported (currently only used in volume control)
-3 = item not found (playlist searching and playing)
-4 = improper command (in repeat)
'''

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=c_id,
    client_secret=c_secret,
    redirect_uri="http://localhost:1507",
    scope="user-modify-playback-state user-read-playback-state playlist-modify-private playlist-modify-public user-read-recently-played"))

devices = sp.devices()
if not devices['devices']:
    print("No active devices found. Make sure a device is active and connected to Spotify.")
else:
    for device in devices['devices']:
        did = device['id']
        print(f"Name: {device['name']}, ID: {device['id']}")

# user = sp.current_user()
# print("User ID:", user['id'])


def info():
    #stuff = sp.current_playback(market=None, additional_types=None)
    stuff = sp.current_playback()
    for thing in stuff:
        print(thing)
        if type(stuff[thing]) == dict:
            for i in stuff[thing]:
                print(i, "\n", stuff[thing][i])
        else:
            print(stuff[thing])
        print()

def playSong():
    if 'resuming' not in sp.current_playback()['actions']['disallows']:    
        try:
            sp.start_playback(device_id=did)
        except:
            return -1
        return 1
    return 0

def pauseSong():
    if 'pausing' not in sp.current_playback()['actions']['disallows']:
        try:
            sp.pause_playback(device_id=did)
        except Exception as e:
            print ("\n",e, "\n")
            return -1
        return 1
    return 0

def skipSong():
    if 'skipping_next' not in sp.current_playback()['actions']['disallows']:
        try:
            sp.next_track(device_id=did)
        except:
            return -1
        return 1
    return 0

def previousSong():
    if 'skipping_previous' not in sp.current_playback()['actions']['disallows']:
        try:
            sp.previous_track(device_id=did)
        except:
            return -1
        return 1
    return 0

def shuffle(state):
    if state != sp.current_playback()['shuffle_state']:
        try:
            sp.shuffle(state, device_id=did)
        except:
            return -1
        return 1
    return 0

# Takes any string input including "" which defaults to track repeat 
# Some additional words are added for more common terms that are changed to the appropriate string
def repeat(state):
    keywords = ["off","track","context","playlist","song", ""]
    if state not in keywords:
        return -4
    if state == "song":
        state = "track"
    elif state == "playlist":
        state = "context"
    elif state == "off":
        state = "off"
    if state != sp.current_playback()['repeat_state']:
        try:
            sp.repeat(state, device_id= did)
        except:
            return -1
        return 1
    return 0

def seekTo(time):
    try:
        sp.seek_track(position_ms=time*1000, device_id=did)
    except:
        return 0
    return 1

def volumeUp():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        try:
            if temp['volume_percent'] > 89:
                sp.volume(100)
                return 1
            elif temp['volume_percent'] == 100:
                return 0
            else:
                sp.volume(temp['volume_percent']+10)
                return 1
        except:
            return -1
    print("Current device doesn't support volume control")
    return -2

def volumeDown():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        try:
            if temp['volume_percent'] < 11:
                sp.volume(0)
                return 1
            elif temp['volume_percent'] == 0:
                return 0
            else:
                sp.volume(temp['volume_percent']-10)
                return 1
        except:
            return -1
    print("Current device doesn't support volume control")
    return -2

def mute():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        if temp['volume_percent'] != 0:    
            try:
                sp.volume(0)
                return 1
            except:
                return -1
        return 0
    print("Current device doesn't support volume control")
    return -2

def maxVolume():
    temp = sp.current_playback()['device']
    if temp['supports_volume']:
        if temp['volume_percent'] != 100:    
            try:
                sp.volume(100)
                return 1
            except:
                return -1
        return 0
    print("Current device doesn't support volume control")
    return -2

def createPlaylist(name, isPublic=False, isCollab=False, desc=""):
    try:
        sp.user_playlist_create(uid, name, isPublic, isCollab, desc)
    except:
        return 0
    return 1

# Takes any string input as name of playlist to be added to
def addCurrentSongToPlaylist(name):
    playlists = [(p['name'].lower(), p['id']) for p in sp.current_user_playlists()['items']]
    selected = [playlist for playlist in playlists if name == playlist[0]]
    currentSong = sp.current_playback()['item']
    if selected:
        try:
            sp.playlist_add_items(selected[0][1],[currentSong['id']],0)
            return 1
        except:
            return -1
    else:
        selected = [playlist for playlist in playlists if name in playlist[0]]
        if selected:
            try:
                sp.playlist_add_items(selected[0][1],[currentSong['id']],0)
                return 1
            except:
                return -1
        else:
            #print(f"No playlist containing {name} found")
            return -3


def addPreviousSongToPlaylist(name):
    playlists = [(p['name'].lower(), p['id']) for p in sp.current_user_playlists()['items']]
    selected = [playlist for playlist in playlists if name == playlist[0]]
    lastSong = sp.current_user_recently_played(limit=1)['items'][0]['track']
    if selected:
        try:
            sp.playlist_add_items(selected[0][1],[lastSong['id']],0)
            return 1
        except:
            return -1
    else:
        selected = [playlist for playlist in playlists if name in playlist[0]]
        if selected:
            try:
                sp.playlist_add_items(selected[0][1],[lastSong['id']],0)
                return 1
            except:
                return -1
        else:
            #print(f"No playlist containing {name} found")
            return -3


# Takes any string input as name of playlist to be played
def playPlaylist(name):
    playlists = [(p['name'].lower(), p['uri']) for p in sp.current_user_playlists()['items']]
    selected = [playlist for playlist in playlists if name == playlist[0]]
    if selected:
        try:
            sp.start_playback(device_id=did, context_uri=selected[0][1])
            return 1
        except:
            return -1
    else:
        selected = [playlist for playlist in playlists if name in playlist[0]]
        if selected:
            try:
                sp.start_playback(device_id=did, context_uri=selected[0][1])
                return 1
            except:
                return -1
        else:
            #print(f"No playlist containing {name} found")
            return -3

def main():
    print("Spotify is working")

if __name__ == "__main__":
    main()