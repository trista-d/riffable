"""
Django will run the function that corresponds with the name of the current path (see search/urls.py).
This allows different pages of the site to do different things.

For more info: https://docs.djangoproject.com/en/3.1/ref/class-based-views/base/#django.views.generic.base.View
"""

import requests
import librosa
import pafy
import re
import os

from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect

# runs on index.html page. Performs search using YouTube API/displays results
def index(request):
    videos = [] # set to empty so nothing happens if API request not sent
    
    # if search bar has been used
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        message = '' # error message
        video_ids = [] # each video's unique id used in URLs
        
        # perform youtube search if daily API quota hasn't been reached
        # more info here: https://developers.google.com/youtube/v3/determine_quota_cost  
        try:
        
            # YouTube search API request parameters
            # more info here: https://developers.google.com/youtube/v3/docs/search/list
            search_params = {
                'part' : 'snippet',
                'q' : request.POST['search'],
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'maxResults' : 48,
                'type' : 'video',
                'videoEmbeddable' : 'true',
                'videoSyndicated' : 'true'
            }
            
            # send request to API using above parameters
            r = requests.get(search_url, params=search_params)
            results = r.json()['items']
            
            # save each video's unique id
            for result in results:
                video_ids.append(result['id']['videoId'])

            if request.POST['submit'] == 'lucky':
                return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
            
            # YouTube API request parameters to get video specifics
            # more info here: https://developers.google.com/youtube/v3/docs/videos/list
            video_params = {
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'part' : 'snippet,contentDetails',
                'id' : ','.join(video_ids),
                'maxResults' : 48
            }
                
            # send request to API using above parameters
            r = requests.get(video_url, params=video_params)
            results = r.json()['items']
                           
        except:
            
            # set API quota error message
            message = 'Sorry, it looks like the site has exceeded its daily quota for Youtube API requests. The site will be operable when the quota resets back to zero at midnight PST. Try again tomorrow!'
            
            # variables to be used in play.html
            context = {
                'message': message, # error message
                'display' : 'none' # unable to show video, so hide iframe
            }
            # go to play.html and display error message...
            return render(request, 'search/play.html', context)

        # ...otherwise display search results    
        
        # save each video's specific details (gotten from 2nd API response)
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data) 
    
    # variables to be used in HTML
    context = {
        'videos' : videos, # dict made of video_data. Used in index.html
        'display' : 'block' # API request was successfu, so show iframe. Used in play.html
    }
    # stay on index.html and display videos with their titles & durations
    return render(request, 'search/index.html', context)
    
# runs on play.html page. Embeds video in page/finds & displays chords
def play(request):
    
    # if view button on a video in index.html has been pressed
    if request.POST:
    
        # get video's unique id & construct embed link
        vid_id = request.POST.get('view')
        embed_url = f'https://www.youtube.com/embed/{ vid_id }?origin=https://triceratops.pythonanywhere.com'
        
        # get the song's audio using pafy as a part of the youtube-dl package 
        # (code is a modified version of: https://github.com/csteinmetz1/youtube-audio-dl/blob/master/youtube-audio-dl.py)
        audio = pafy.new(f'https://www.youtube.com/watch?v={ vid_id }')
        audio_stream = audio.getbestaudio(preftype="m4a", ftypestrict=True)
        filename = re.sub("[^a-zA-Z0-9_ ]", "", audio.title)
        filename = re.sub("[ ]", "_", filename)
        filepath = os.path.join(filename + ".m4a")
        audio_output = audio_stream.download(filepath=filepath)
        
        #format it so librosa can analyze it
        stream = librosa.stream(filename + '.m4a', block_length=256, frame_length=4096, hop_length=4096)
        
        # remove audio after analyzing it
        os.remove(filename + '.m4a') 
        
        # variables to use in play.html
        context = {
            'embed' : embed_url # embed link for iframe
        }
    
    # if the view button hasn't been pressed (page was reloaded) do nothing
    else:
        context = {} 
    
    # stay on play.html & change HTML based on context  
    return render(request, 'search/play.html', context)