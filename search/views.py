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
import subprocess

import numpy as np

#uncomment to visually see mel spectrogram
# import librosa.display
# import matplotlib.pyplot as plt

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
                'videoSyndicated' : 'true',
                'videoDuration' : 'medium'
            }
            
            # send request to API using above parameters
            r = requests.get(search_url, params=search_params)
            results = r.json()['items']
            
            # save each video's unique id
            for result in results:
                video_ids.append(result['id']['videoId'])
            
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
        # https://librosa.org/doc/main/ioformats.html
        audio = pafy.new(f'https://www.youtube.com/watch?v={ vid_id }')
        audio_stream = audio.getbestaudio(preftype="m4a", ftypestrict=True)
        filename = re.sub("[^a-zA-Z0-9_ ]", "", audio.title)
        filename = re.sub("[ ]", "_", filename)
        filepath = os.path.join(filename + ".m4a")
        audio_output = audio_stream.download(filepath=filepath)
        
        filepath = filename + '.m4a'
        
        #frame_length = (2048 * sr)
        #hop_length = (512 * sr)
        
        hop_length = 512
        
        #load the actual audio into librosa
        y, sr = librosa.load(filepath)
        
        # create a mel spectrogram
        # more info: https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
        # https://towardsdatascience.com/getting-to-know-the-mel-spectrogram-31bca3e2d9d0
        filter_banks = librosa.filters.mel(n_fft=2048, sr=22050, n_mels=90)
        #filter_banks.shape
        
        mel_spectrogram = librosa.feature.melspectrogram(y, sr=sr, n_fft=2048, hop_length=hop_length, n_mels=90)
        mel_spectrogram.shape
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
        
        # uncomment to visually see mel spectrogram
        """
        plt.figure(figsize=(25, 10))
        librosa.display.specshow(log_mel_spectrogram, x_axis='time', y_axis='mel', sr=sr)
        plt.colorbar(format='%+2.f')
        plt.show()
        """
        
        """
        To get chords:
            1. analyze spectrogram for consonant note ratios (3:2, 5:4 etc.)
            2. Based on the frequencies (Hz) of these notes, assign them proper names (C, A, G# etc.)
            3. Use a library (Mingus is a possible option? Or pychord) to take these groups of notes as input
               then output a matching chord name
               https://softwarerecs.stackexchange.com/questions/69576/python-library-to-detect-chords-from-notes
            4. use a library or API to get images of chord charts to display on a scrolling sidebar in play.html
            5. This might take a while so show the user a loading screen while chords are being generated
               and use play.html only for embedding the video and displaying the chords?
            6. but how would alternate guitar tunings work?
        """
        
        # remove audio after analyzing it
        os.remove(filepath) 
        
        # variables to use in play.html
        context = {
            'embed' : embed_url # embed link for iframe
        }
        
    # if view button hasn't been pressed (page was reloaded so video is already there) do nothing
    else:
        context = {} 
    # stay on play.html & change HTML based on context  
    return render(request, 'search/play.html', context)