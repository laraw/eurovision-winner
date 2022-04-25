import song_data as sg
import pandas as pd
import utils

def get_song_data(title, artist):
    
    return sg.Song(title, artist)

def get_genre(songdata):
    try:
        genre = songdata.genre
        return genre
    except AttributeError:
        return ""

def get_language(songdata):
    try:
        language = songdata.language
        return language
    except AttributeError:
        return ""

#richdata - sf_number	sf_score	betting_odds	language	act_type	YT_likes	YT_comments	YT_positive_comments	YT_negative_comments	lyrics_type	ev_poll_result	previous_winner_cnt	previous_runner_up_cnt
def enrich_data():  
    winners = pd.read_csv("song_data.csv")
    #winners['songdata'] = (winners['song'],winners['performer']).apply(get_song_data)
    winners['songdata'] = winners[['song','performer']].apply(lambda x: get_song_data(*x), axis=1)
    winners['genre'] = winners['songdata'].apply(get_genre)
    winners['language'] =  winners['songdata'].apply(get_language)
    winners.drop('songdata', axis=1, inplace=True)
    winners.to_csv("song_data_enriched.csv")

songs = pd.read_csv("song_data.csv")

songs['performer'] = songs['performer'].apply(utils.remove_non_alpha)
songs['song'] = songs['song'].apply(utils.remove_non_alpha)
songs['composers'] = songs['composers'].apply(utils.remove_non_alpha)
songs['lyricists'] = songs['lyricists'].apply(utils.remove_non_alpha)
songs['lyrics'] = songs['lyrics'].apply(utils.remove_non_alpha)

print(songs['composers'])
#songs.to_csv("song_data_cleansed.csv")