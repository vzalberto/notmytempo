from flask import Flask, render_template, request
import spotipy
from spotipy import oauth2 as OA2
import os

#import config

app = Flask(__name__)


token   =   OA2.SpotifyClientCredentials(os.environ['SPOTIPY_CLIENT_ID'], os.environ['SPOTIPY_CLIENT_SECRET'])
auth    =   token.get_access_token()

sp = spotipy.Spotify(auth)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['query'] != None:
            results = sp.search(q=request.form['query'])
            if results['tracks']:
                return render_template('trackInfo.html', results=results['tracks']['items'])
            else:
                return "NOPE"
    return render_template('index.html')

@app.route('/artist/<artist>')
def searchArtist(artist):
    results = sp.search(q=artist, limit=20, type='artist')
    return render_template('artist.html', results=results['artists']['items'])

@app.route('/track/<id>')
def getRhythm(id):
    track = sp.audio_features([id])
    return render_template('track.html', track=track)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
