# clip-watcher

Grava uma live, conta o chat a cada 10s, corta 30/60s em volta dos picos (9:16) e põe legenda em português com destaque palavra por palavra. Sem conta, sem token.

## Requisitos
`pip install streamlink faster-whisper` e `ffmpeg`.

## Uso
    ./watch.sh CANAL          # durante a live (Ctrl+C ao fim)
    ./watch.sh --clip CANAL   # gera 5 clipes de 30s e 5 de 60s em runs/CANAL/clips

Só Twitch lê o chat. Em VOD ou outras plataformas, `peaks.py` usa o volume do áudio.
Peça permissão ao streamer antes de postar os clipes.
