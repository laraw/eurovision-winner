import requests
from dataclasses import dataclass
from langdetect import detect

MUSICMATCH_API_KEY = "6d5f621b438b1304a7970bc1bd5e40c2"
MUSICMATCH_APP_NAME = "Larbot Apps's App"
# musixmatch api base url
BASE_URL = "https://api.musixmatch.com/ws/1.1/"
API_KEY_STR = "&apikey=" + MUSICMATCH_API_KEY
FORMAT_URL = "?format=json&callback=callback"
SEARCH_TRACKS = "/track.search"
LYRICS_GET = "/track.lyrics.get"
LYRICS_MOOD_GET = "/track.lyrics.mood.get"
class Song:
    title: str
    artist: str
    lyrics: str
    genre: str
    trackId: int
    commontrackId: int
    language: str
    #mood: str
    #lyricType: str
    

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        
        self.trackId, self.genre, self.commontrackId = search_track(artist, title)
        if(self.trackId != None):
            self.lyrics = search_lyrics(self.trackId)
            self.language = detect(self.lyrics)

def get_parameter_string(parameters):
    parameterString = "&"
    if(len(parameters) > 0):
        for i, p in enumerate(parameters):
            parameterString += p["name"] + "=" + str(p["value"]) 
            if i != len(parameters)-1:
                parameterString += "&"

    return parameterString



def search_lyrics(trackId):
    
    parameters = []
    parameters.append({
        "name": "track_id",
        "value": trackId
    })
    api_call = BASE_URL + LYRICS_GET + FORMAT_URL + get_parameter_string(parameters) + API_KEY_STR

    request = requests.get(api_call)
    data = request.json()

    try:
        return data.get("message").get("body").get("lyrics").get("lyrics_body")
    except:
        return ""


# def lyrics_mood(commontrackId):
#     parameters = []
#     parameters.append({
#         "name": "commontrack_id",
#         "value": commontrackId
#     })
#     api_call = BASE_URL + LYRICS_MOOD_GET + FORMAT_URL + get_parameter_string(parameters) + API_KEY_STR

#     request = requests.get(api_call)
#     data = request.json()
#     print(data)
#     #lyricsmood = data.get("message").get("body").get("mood_list")
#     #print(lyricsmood)
#     return ""

def search_track(artist, title):
    parameters = []
    
    parameters.append({
        "name": "q_artist",
        "value":  artist,
    
    })

    parameters.append({
        "name": "q_track",
        "value":  title,
    
    })
    api_call = BASE_URL + SEARCH_TRACKS + FORMAT_URL + get_parameter_string(parameters) + API_KEY_STR
    
    request = requests.get(api_call)
    data = request.json()
    
    tracklist = data.get("message").get("body").get("track_list")
    
    if(len(tracklist) > 0):
       
        track = tracklist[0].get("track")
        trackId = track.get("track_id")
        genres = track.get("primary_genres").get("music_genre_list")
        genre = ""
        if(len(genres) > 0):
            genre = genres[0].get("music_genre").get("music_genre_name")
        commontrackId = track.get("commontrack_id")
        return trackId, genre, commontrackId 
    else:
        return None, None, None
    

#Song("Zitti E Buoni", "Maneskin")
