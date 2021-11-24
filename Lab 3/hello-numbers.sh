
   
#!/bin/sh

echo "What year were you born?" | festival --tts

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 3 -t wav recorded_mono-hello-numbers.wav
python3 numbers.py recorded_mono-hello-numbers.wav