"""Whisper -> legenda ASS com destaque palavra por palavra (estilo karaokê, 9:16)."""
import json, sys

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,DejaVu Sans,84,&H00FFFFFF,&H0000C8FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,2,2,60,60,520,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""


def ts(s):
    h, m = int(s // 3600), int(s % 3600 // 60)
    return f"{h}:{m:02d}:{s % 60:05.2f}"


def build(words, offset=0.0, per_line=3):
    """words: [(start, end, texto)] em segundos do vídeo original. offset = início do clipe."""
    ev = []
    for i in range(0, len(words), per_line):
        grp = words[i:i + per_line]
        gs, ge = grp[0][0] - offset, grp[-1][1] - offset
        if ge <= 0:
            continue
        for j, (s, e, w) in enumerate(grp):  # uma linha de evento por palavra ativa
            parts = [
                (r"{\c&H0000C8FF&\fscx115\fscy115}" if k == j else r"{\c&H00FFFFFF&}") + x[2].strip().upper()
                for k, x in enumerate(grp)
            ]
            a = max(s - offset, 0)
            b = (grp[j + 1][0] - offset) if j + 1 < len(grp) else (e - offset)
            ev.append(f"Dialogue: 0,{ts(a)},{ts(max(b, a + 0.05))},Default,,0,0,0,,{' '.join(parts)}")
    return HEADER + "\n".join(ev) + "\n"


if __name__ == "__main__":
    words = json.load(open(sys.argv[1]))
    offset = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    sys.stdout.write(build(words, offset))
