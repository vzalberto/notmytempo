# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo
import spotipy
from spotipy import oauth2 as OA2
import os

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ['MONGO_URI']
mongo = PyMongo(app)

token   =   OA2.SpotifyClientCredentials(os.environ['SPOTIPY_CLIENT_ID'], os.environ['SPOTIPY_CLIENT_SECRET'])
auth    =   token.get_access_token()

sp = spotipy.Spotify(auth)

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
    track = sp.audio_features([id])
    mongo.db.searches.insert_one({'track_id':id, 'ip':request.remote_addr})
    return render_template('track.html', track=track, keys=keys, modes=modes)

@app.route('/analysis/<id>')
def getAnalysis(id):
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'B#']
    modes = ['minor', 'Major']
    analysis = sp.audio_analysis(id)
    #mongo.db.searches.insert_one({'track_id':id, 'ip':request.remote_addr})
    return render_template('analysis.html', analysis=analysis, keys=keys, modes=modes)

@app.route('/stats')
def getStats():
    searches = mongo.db.searches.find()
    return render_template('stats.html',searches=searches)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
