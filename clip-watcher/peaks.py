"""Acha picos de atividade. Aceita chat (jsonl) ou, sem chat, picos de volume do áudio."""
import json, subprocess, sys, re


def from_chat(path):
    return [(r["t"], r["n"]) for r in map(json.loads, open(path))]


def from_audio(video, bucket=10):
    """Fallback p/ VOD: energia média do áudio por janela de `bucket` segundos."""
    cmd = ["ffmpeg", "-v", "info", "-i", video, "-vn", "-af",
           f"asetnsamples=n=48000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
           "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    vals = [float(x) for x in re.findall(r"RMS_level=(-?[\d.]+|-inf)", err.replace("-inf", "-90"))]
    out = []
    for i in range(0, len(vals), bucket):
        w = vals[i:i + bucket]
        out.append((i, sum(w) / len(w) + 90))  # desloca p/ positivo
    return out


def top_peaks(series, k, min_gap, clip_len):
    """k maiores picos, separados por >= min_gap s. Devolve tempos centrais."""
    chosen = []
    for t, v in sorted(series, key=lambda x: -x[1]):
        if v <= 0 or any(abs(t - c) < min_gap for c, _ in chosen):
            continue
        chosen.append((t, v))
        if len(chosen) == k:
            break
    return sorted(c for c, _ in chosen)


if __name__ == "__main__":
    src, k = sys.argv[1], int(sys.argv[2])
    series = from_chat(src) if src.endswith(".jsonl") else from_audio(src)
    print(json.dumps(top_peaks(series, k, min_gap=60, clip_len=30)))
