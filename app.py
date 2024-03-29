# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
# from flask.ext.pymongo import PyMongo
import spotipy
from spotipy import oauth2 as OA2
from spotipy.oauth2 import SpotifyClientCredentials
import os
import datetime

app = Flask(__name__)
#app.run(debug=True)
# app.config['MONGO_URI'] = os.environ['MONGO_URI']
# mongo = PyMongo(app)

"""
token   =   OA2.SpotifyClientCredentials(os.environ['SPOTIPY_CLIENT_ID'], os.environ['SPOTIPY_CLIENT_SECRET'])
auth    =   token.get_access_token()

sp = spotipy.Spotify(auth)
"""
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['query']:
            results = sp.search(q=request.form['query'])
            if results['tracks']['items']:
                return render_template('trackInfo.html', results=results['tracks']['items'])
            else:
                return render_template('index.html', error=1, query=request.form['query'])
    return render_template('index.html')

@app.route('/artist/<artist>')
def searchArtist(artist):
    results = sp.search(q=artist, limit=20, type='artist')
    return render_template('artist.html', results=results['artists']['items'])

@app.route('/track/<id>')
def getRhythm(id):
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'B#']
    modes = ['minor', 'Major']
    track_features = sp.audio_features([id])
    track = sp.track(id)

    ## mongo.db.searches.insert_one({'track_id':id, 'track_name':track['name'], 'artist':track['artists'][0]['name'], 'date': datetime.datetime.now(), 'ip':request.remote_addr})
    return render_template('track.html', track=track_features, keys=keys, modes=modes)

@app.route('/analysis/<id>')
def getAnalysis(id):
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'B#']
    modes = ['minor', 'Major']
    analysis = sp.audio_analysis(id)
    return render_template('analysis.html', analysis=analysis, keys=keys, modes=modes, id=id)

@app.route('/stats')
def getStats():
    #searches = mongo.db.searches.find().sort("date",-1)
    #count = searches.count()
    #return render_template('stats.html',searches=searches,count=count) """
    return render_template('stats.html',searches=[],count=0)

@app.route('/test')
def test():
    new_releases = sp.new_releases(limit=50)
    return render_template('test.html', new_releases=new_releases)

@app.route('/playlist/<id>')
def playlist(id):
    items = sp.playlist_items(id)
    return render_template('playlist_items.html', items=items)

@app.route('/user/<id>')
def user(id):
    user = sp.user(id)
    playlists = sp.user_playlists(id)
    return render_template('user_playlists.html', user=user, playlists=playlists )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
