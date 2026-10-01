import sys, json
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, info = m.transcribe(src, word_timestamps=True, vad_filter=True, beam_size=5)
res = []
with open(out + ".txt", "w", encoding="utf-8") as f:
    for s in segs:
        f.write(f"[{s.start:7.2f} - {s.end:7.2f}] {s.text.strip()}\n"); f.flush()
        res.append({"start": s.start, "end": s.end, "text": s.text,
                    "words": [{"s": w.start, "e": w.end, "w": w.word} for w in s.words]})
json.dump(res, open(out + ".json", "w", encoding="utf-8"), indent=1)
print("done")
