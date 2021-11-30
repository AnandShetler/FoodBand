from flask import Flask, render_template
from flask.helpers import send_file, send_from_directory
from midiutil import MIDIFile

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create-midi")
def create_midi():
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

    with open("major-scale.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
    return send_file("major-scale.mid", as_attachment=True, mimetype="audio/midi")