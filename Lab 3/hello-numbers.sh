
   
#!/bin/sh

echo "What year were you born?" | festival --tts

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 3 -t wav recorded_mono.wav
python3 get_number.py recorded_mono.wav