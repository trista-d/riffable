from isodate import parse_duration
import requests
import pafy
import re
import os

# A wrapper for Chordino from https://github.com/ohollo/chord-extractor
from chord_extractor.extractors import Chordino

# way to generate chord charts from https://smus.com/generating-guitar-chord-diagrams/
from chords import CHORDS, filenames, export_chords

# file that stores your youtube api key
import config

from flask import Flask, render_template, request
from . import app


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    #print(request.form['search'])
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
                'q' : request.form['search'],
                'key' : config.api_key,
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
                'key' : config.api_key,
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
            return render_template('play.html', message=message, display='none')

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
    # stay on index.html and display videos with their titles & durations
    return render_template('index.html', videos=videos)

# runs on play.html page. Embeds video in page/finds & displays chords
@app.route("/play", methods=["POST"])
def play():
    # if view button on a video in index.html has been pressed
    if request.method == "POST" :
       
        # get video's unique id & construct embed link
        vid_id = request.form['view']
        embed_url = f'https://www.youtube.com/embed/{ vid_id }?origin=?triceratops.pythonanywhere.com'
        
        # get the song's audio using pafy as a part of the youtube-dl package
        # (code is a modified version of: https://github.com/csteinmetz1/youtube-audio-dl/blob/master/youtube-audio-dl.py)
        audio = pafy.new(vid_id)
        audio_stream = audio.getbestaudio(preftype="m4a", ftypestrict=True)
        filename = re.sub("[^a-zA-Z0-9_ ]", "", audio.title)
        filename = re.sub("[ ]", "_", filename)
        filepath = os.path.join(filename + ".m4a")
        try :
            audio_output = audio_stream.download(filepath=filepath)
        except:
            return render_template('index.html') 
        filepath = filename + '.m4a'

        # use to Chordino to get chords
        # Info on parameters: http://www.isophonics.net/nnls-chroma
        chordino = Chordino()
        chord = chordino.extract(filepath)

        # remove audio after analyzing it
        os.remove(filepath)

        # prevent future 403 error
        os.system("youtube-dl --rm-cache-dir")

        # remove repeated chords and non-chords
        notes = []
        for note in chord :
            if note[0] != "N" and note[0] not in notes :
                notes.append(note[0])
        
        # get chord fingerings
        fingerings = {}
        for note in notes :
            if note in CHORDS :
                fingerings[note] = CHORDS[note]
        
        export_chords('static/images/', fingerings)

        # variables to use in play.html
        context = {
            'embed' : embed_url, # embed link for iframe
            'display': 'block',
            "fingerings": filenames
        }

        # stay on play.html & change HTML based on context  
        return render_template("play.html", display=context["display"], embed=context["embed"], fingerings=context['fingerings'])