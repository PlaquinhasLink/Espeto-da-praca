"""Transcreve com faster-whisper (pt) e salva palavras com tempo: [(ini, fim, palavra)]."""
import json, sys
from faster_whisper import WhisperModel

model = WhisperModel("small", compute_type="int8")
segs, _ = model.transcribe(sys.argv[1], language="pt", word_timestamps=True)
words = [(round(w.start, 2), round(w.end, 2), w.word) for s in segs for w in s.words]
json.dump(words, open(sys.argv[2], "w"), ensure_ascii=False)
