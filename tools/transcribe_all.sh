#!/usr/bin/env bash
# Chunked study transcription: 10-min wavs -> one-shot tiny whisper -> merge.
# Keeps RSS bounded on small boxes (sustained runs get OOM-killed).
set -u
D=/root/tantrasara
SRC=$D/sources/lectures/audio/study
OUT=$D/sources/lectures/transcripts-study
TMP=/tmp/study_chunks
mkdir -p "$OUT" "$TMP"
names="wallis_01 wallis_02 wallis_03 wallis_04 wallis_05 wallis_06 wallis_07 wallis_08 wallis_09"
keys="wallis-three-effective-methods wallis-ch5-part3 wallis-ch5-part2 wallis-ch5-part1 wallis-ch4-part2 wallis-ch4-part1 wallis-ch3-abridged wallis-ch2 wallis-ch1"
i=0
for n in $names; do
  i=$((i+1)); key=$(echo $keys | cut -d' ' -f$i)
  dst="$OUT/$key.transcript.json"
  if [ -f "$dst" ] && [ $(stat -c%s "$dst") -gt 1000 ]; then echo "have $key"; continue; fi
  echo "=== $key ==="
  rm -f $TMP/c_*.wav $TMP/p_*.json
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC/$n.mp3")
  start=0; idx=0
  while [ $(echo "$start < $dur" | bc) -eq 1 ]; do
    ffmpeg -v error -y -ss $start -to $(echo "$start+600" | bc) -i "$SRC/$n.mp3" -ar 16000 -ac 1 -c:a pcm_s16le "$TMP/c_$idx.wav"
    python3 $D/tools/transcribe_chunk.py "$TMP/c_$idx.wav" "$TMP/p_$idx.json" $start || exit 1
    rm -f "$TMP/c_$idx.wav"
    sleep 5
    start=$(echo "$start+600" | bc); idx=$((idx+1))
  done
  python3 -c "
import json, glob
ss=[]
for f in sorted(glob.glob('$TMP/p_*.json'), key=lambda x: int(x.split('_')[-1].split('.')[0])):
    ss += json.load(open(f))['sentences']
out={'source':'$n.mp3','duration':$dur,'engine':'faster-whisper tiny (study-only; small.en at canon time)','sentences':ss}
json.dump(out, open('$dst','w'), indent=1)
print('wrote $key', len(ss), 'sentences')"
  rm -f $TMP/p_*.json
done
echo ALLDONE
