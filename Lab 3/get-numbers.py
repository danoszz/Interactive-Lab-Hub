#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import json
import sys

SetLogLevel(0)

if not os.path.exists("small_model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'small_model' in the current folder.")
    exit (1)

wf = open(sys.argv[1], "rb")
wf.read(44) # skip header

model = Model("small_model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, 16000) #, "zero oh one two three four five six seven eight nine".split())

while True:
    data = wf.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        print (res['text'])

res = json.loads(rec.FinalResult())
print (res['text'])