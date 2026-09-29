#!/usr/bin/env bash
# 20-second vertical Reel/TikTok from the 2-minute smoker clip (720x1280).
# Usage: scripts/smoker_reel.sh <source.mp4> <endcard.png> [out.mp4]
# Four captioned shots (steadied, colour-lifted, slow zoom) + a 3.5 s end card,
# joined with 0.4 s crossfades; audio is the original fire crackle, loudness-normalised.
# Captions sit at y=1110-1360 to stay clear of the TikTok/Reels button area.
set -euo pipefail
V="$1"; END="$2"; OUT="${3:-fudi-smoker-reel.mp4}"
F=/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf
TMP=$(mktemp -d)

clip() { # name start duration "caption"
  ffmpeg -v error -y -ss "$2" -t "$3" -i "$V" -filter_complex "\
[0:v]deshake,scale=1188:2112,\
zoompan=z='1+0.0015*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,\
eq=saturation=1.18:contrast=1.06:brightness=0.01,\
drawbox=x=0:y=1110:w=iw:h=250:color=black@0.35:t=fill,\
drawtext=fontfile=$F:text='$4':fontsize=86:fontcolor=0xFFF3E2:x=(w-tw)/2:y=1180:\
shadowcolor=black@0.6:shadowx=3:shadowy=3:alpha='if(lt(t,0.3),t/0.3,1)'[v];\
[0:a]afade=t=in:d=0.3,afade=t=out:st=$(echo "$3-0.4" | bc):d=0.4[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -ar 44100 -ac 2 "$TMP/$1.mp4"
}

clip c1 1.5 4 "Low heat."
clip c2 61  4 "Hours of smoke."
clip c3 84  6 "Real fire. No shortcuts."
clip c4 70  4 "Grown on our farm."
ffmpeg -v error -y -loop 1 -t 3.5 -i "$END" -f lavfi -t 3.5 -i anullsrc=r=44100:cl=stereo \
  -vf "fps=30,format=yuv420p,fade=t=in:d=0.4" -c:v libx264 -crf 18 -c:a aac -shortest "$TMP/c5.mp4"

X=0.4
ffmpeg -v error -y -i "$TMP/c1.mp4" -i "$TMP/c2.mp4" -i "$TMP/c3.mp4" -i "$TMP/c4.mp4" -i "$TMP/c5.mp4" \
  -filter_complex "\
[0:v][1:v]xfade=transition=fade:duration=$X:offset=3.6[v1];\
[v1][2:v]xfade=transition=fade:duration=$X:offset=7.2[v2];\
[v2][3:v]xfade=transition=fade:duration=$X:offset=12.8[v3];\
[v3][4:v]xfade=transition=fade:duration=$X:offset=16.4[v];\
[0:a][1:a]acrossfade=d=$X[a1];[a1][2:a]acrossfade=d=$X[a2];[a2][3:a]acrossfade=d=$X[a3];\
[a3][4:a]acrossfade=d=$X,loudnorm=I=-16:TP=-1.5[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 19 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k "$OUT"
rm -rf "$TMP"
