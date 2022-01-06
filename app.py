from flask import Flask, render_template, request
from flask.helpers import send_file
from midiutil import MIDIFile

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create-midi")
# input format: 1D?? list of ALL tracks containing note tuples of (fruit, x, y)??
def create_midi(tracks):
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 60   # In BPM
    volume   = 100
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI.addTempo(track, time, tempo)
    for i, pitch in enumerate(degrees):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    tracks = request.json
    midiFile = MIDIFile(len(tracks))
    trackNum = 0
    for track in tracks:
        midiFile.addTempo(trackNum, 0, 60)
        for note in track:
            midiFile.addNote(trackNum, channel, note[0], note[1], duration, volume)
        trackNum += 1


    with open("major-scale.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
    return send_file("major-scale.mid", as_attachment=True, mimetype="audio/midi")