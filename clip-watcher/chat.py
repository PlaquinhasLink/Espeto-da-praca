"""Leitor anônimo do chat da Twitch (sem conta, sem token) + contador a cada 10s.

Uso: python3 chat.py CANAL SAIDA.jsonl
Cada linha: {"t": segundos_desde_o_inicio, "n": mensagens_na_janela}
"""
import json, socket, sys, time

BUCKET = 10  # segundos


def main(channel, out_path):
    channel = channel.lower().lstrip("#")
    start = time.time()
    sock = socket.create_connection(("irc.chat.twitch.tv", 6667), timeout=30)
    sock.sendall(b"PASS SCHMOOPIIE\r\nNICK justinfan12345\r\n")
    sock.sendall(f"JOIN #{channel}\r\n".encode())
    sock.settimeout(1.0)
    buf, count, bucket_start = "", 0, 0
    with open(out_path, "a") as out:
        while True:
            try:
                data = sock.recv(8192).decode("utf-8", "ignore")
                if not data:
                    raise ConnectionError("chat fechou")
                buf += data
                *lines, buf = buf.split("\r\n")
                for ln in lines:
                    if ln.startswith("PING"):
                        sock.sendall(b"PONG :tmi.twitch.tv\r\n")
                    elif " PRIVMSG " in ln:
                        count += 1
            except socket.timeout:
                pass
            now = int(time.time() - start)
            if now - bucket_start >= BUCKET:
                out.write(json.dumps({"t": bucket_start, "n": count}) + "\n")
                out.flush()
                bucket_start, count = bucket_start + BUCKET, 0


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
