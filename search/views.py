import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 48,
            'type' : 'video',
            'videoEmbeddable' : 'true',
            'videoSyndicated' : 'true'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 48
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            
            # save to sessions so data can be accessed in other views
           # request.session['id'] = result['id']

            videos.append(video_data)

    context = {
        'videos' : videos
    }
    return render(request, 'search/index.html', context)
    
# embeds video in page/finds & displays chords
def play(request):
    # get video's unique id & construct embed link
    embed_url = 'https://www.youtube.com/embed/' + request.POST.get('view') + "&enablejsapi=1&origin=https%3A%2F%2triceratops.pythonanywhere.com&widgetid=1"

    context = {
        'embed' : embed_url
    }
    return render(request, 'search/play.html', context)
