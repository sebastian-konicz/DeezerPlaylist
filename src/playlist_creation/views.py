from django.shortcuts import render
import pandas as pd
import openpyxl
import requests

# Create your views here.
def index(request):
    if "GET" == request.method:
        return render(request, 'playlist_creation/index.html', {})
    else:
        # getting acces token
        social = request.user.social_auth.get(provider='deezer')
        access_token = social.extra_data['access_token']
        playlist_id = 1703463421
        track_id = 2184743
        print(access_token)
        url = 'http://api.deezer.com/playlist/{playlist_id}>/tracks?access_token={access_token}&request_method=post&songs={track_id}'.format(playlist_id=playlist_id, access_token=access_token, track_id=track_id)
        search_result = requests.get(url).json()
        print(search_result)
        # getting uploaded file
        excel_file = request.FILES["document"]
        excel_data = pd.read_excel(excel_file)
        return render(request, 'playlist_creation/index.html', {"excel_data":search_result})

def playlist_creation():
    paylist_id =
    return playlist_id