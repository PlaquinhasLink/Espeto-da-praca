"""Corta N segundos em volta de um pico, em 9:16 (1080x1920), com legenda ASS queimada."""
import subprocess, sys


def cut(video, center, length, out, ass=None):
    start = max(center - length / 2, 0)
    vf = "split[a][b];[a]scale=1080:1920,boxblur=30[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2"
    if ass:
        vf += f",ass={ass}"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-i", video, "-t", str(length),
                    "-filter_complex", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                    "-c:a", "aac", "-b:a", "160k", out], check=True)
    return start


if __name__ == "__main__":
    video, center, length, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    cut(video, center, length, out, sys.argv[5] if len(sys.argv) > 5 else None)
