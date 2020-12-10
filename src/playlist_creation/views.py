from django.shortcuts import render
import pandas as pd
import openpyxl
import requests

# Create your views here.
def index(request):
    if "GET" == request.method:
        return render(request, 'playlist_creation/index.html', {})
    else:
        # getting uploaded file
        excel_file = request.FILES["document"]
        excel_data = pd.read_excel(excel_file)

        # getting access token
        social = request.user.social_auth.get(provider='deezer')
        access_token = social.extra_data['access_token']
        print(access_token)

        # creating playlist
        playlist_id = playlist_creation()

        # searching for tracks
        id_list = song_search(excel_data)
        print(id_list)

        # creating playlist
        for id in id_list:
            url = 'http://api.deezer.com/playlist/{playlist_id}>/tracks?access_token={access_token}&request_method=post&songs={track_id}'.format(playlist_id=playlist_id, access_token=access_token, track_id=id)
            search_result = requests.get(url).json()
            print(search_result)

        return render(request, 'playlist_creation/index.html', {})

def playlist_creation():
    playlist_id = 8363186522
    return playlist_id

def song_search(excel_data):
    # reanming dataframe
    df = excel_data

    # running search on dataframe
    df["Search"] = df.apply(lambda df: deezer_search(df['Song'], df['Artist']), axis=1)

    # unpacking tuple form search
    df["Artist_deezer"] = df['Search'].apply(lambda df: df[0])
    df["Song_deezer"] = df['Search'].apply(lambda df: df[1])
    df["Song_id_deezer"] = df['Search'].apply(lambda df: df[2])

    id_list = df["Song_id_deezer"].tolist()
    return id_list

def deezer_search(song, artist):
    try:
        url = "https://api.deezer.com/search?q='{song}' '{artist}'".format(song=song, artist=artist)
        search_result = requests.get(url).json()
        song = search_result['data'][0]['title']
        artist = search_result['data'][0]['artist']['name']
        id = search_result['data'][0]['id']
        print(artist, song, id)
    except IndexError:
        artist = ""
        song = ""
        id = ""
    except ValueError:
        artist = ""
        song = ""
        id = ""
    return artist, song, id