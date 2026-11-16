#!/usr/bin/env bash
# Uso: ./watch.sh CANAL            (grava a live + conta o chat; Ctrl+C para parar)
#      ./watch.sh --clip CANAL     (gera os clipes depois)
set -euo pipefail
cd "$(dirname "$0")"
if [ "${1:-}" = "--clip" ]; then
  C="$2"; D="runs/$C"; mkdir -p "$D/clips"
  python3 transcribe.py "$D/live.ts" "$D/words.json"
  for L in 30 60; do
    i=0
    for T in $(python3 peaks.py "$D/chat.jsonl" 5); do
      i=$((i+1)); S=$(python3 -c "print(max($T-$L/2,0))")
      python3 captions.py "$D/words.json" "$S" > "$D/c.ass"
      python3 clip.py "$D/live.ts" "$T" "$L" "$D/clips/${L}s_$i.mp4" "$D/c.ass"
    done
  done
  exit 0
fi
C="$1"; D="runs/$C"; mkdir -p "$D"
python3 chat.py "$C" "$D/chat.jsonl" &  CP=$!
trap 'kill $CP 2>/dev/null || true' EXIT
streamlink --twitch-disable-ads "twitch.tv/$C" best -o "$D/live.ts"
