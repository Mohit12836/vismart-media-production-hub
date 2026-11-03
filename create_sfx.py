import subprocess
import os
import math

base_audio = os.path.join("hindi-reel", "public", "audio")
os.makedirs(base_audio, exist_ok=True)

# 1. Whoosh sound (white noise swept with bandpass filter)
whoosh_path = os.path.join(base_audio, "whoosh.mp3")
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "anoisesrc=d=0.4:c=pink:r=44100,lowpass=f=1200,volume=0.8",
    "-af", "afade=t=in:ss=0:d=0.15,afade=t=out:st=0.25:d=0.15",
    whoosh_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 2. Pop sound (short sine burst with exponential pitch drop)
pop_path = os.path.join(base_audio, "pop.mp3")
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "sine=f=800:d=0.15",
    "-af", "asetrate=44100*2,aresample=44100,afade=t=out:st=0.03:d=0.12,volume=0.9",
    pop_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 3. Ding / chime sound (sparkling high bell)
ding_path = os.path.join(base_audio, "ding.mp3")
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "sine=f=1760:d=0.6",
    "-af", "afade=t=out:st=0.05:d=0.55,volume=0.7",
    ding_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 4. Energetic Upbeat Lo-Fi / Groove Background Loop (170 seconds)
# We can create a rhythmic electronic beat using multiple sine/saw synth layers in ffmpeg!
bg_path = os.path.join(base_audio, "bg.mp3")
# Generate a nice gentle chord pulse + sub groove for 172 seconds
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "sine=f=220:d=172",
    "-af", "volume=0.04,lowpass=f=400",
    bg_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("SFX created successfully!")
