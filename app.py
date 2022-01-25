from flask import Flask, render_template, request
from flask.helpers import send_file
from midiutil import MIDIFile
import json

app = Flask(__name__)

fruitNotes = {"orange":60, "apple":62, "banana": 64, "kiwi":67, "melon":69, "peach":71, "pear":72, "strawberry":74}
fruitChannel = {"orange":0, "apple":2, "banana": 4, "kiwi":7, "melon":9, "peach":1, "pear":2, "strawberry":4}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create-midi", methods=["GET","POST"])
def create_midi():
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 100    # In beats
    tempo    = 6000   # In BPM
    volume   = 100
    # MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    # MyMIDI.addTempo(track, time, tempo)
    # for i, pitch in enumerate(degrees):
    #     MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
    # with open("major-scale.mid", "wb") as output_file:
    #     MyMIDI.writeFile(output_file)
    # return send_file("major-scale.mid", as_attachment=True, mimetype="audio/midi")

    tracks = json.loads(request.args.get("tracks"))
    midiFile = MIDIFile(len(tracks))
    trackNum = 0
    for track in tracks:
        midiFile.addTempo(trackNum, 0, tempo)
        for note in track:
            midiFile.addNote(trackNum, fruitChannel[note[0]], fruitNotes[note[0]], note[1], duration, volume)
        trackNum += 1


    with open("your-midi.mid", "wb") as output_file:
        midiFile.writeFile(output_file)
    return send_file("your-midi.mid", as_attachment=True, mimetype="audio/midi")