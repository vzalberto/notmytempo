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
    track = sp.audio_features([id])
    return render_template('track.html', track=track, keys=keys)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
