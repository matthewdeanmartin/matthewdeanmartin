from __future__ import annotations

import argparse
import contextlib
import http.server
import os
import socket
import socketserver
import threading
import time
import webbrowser
from pathlib import Path


def pick_port(host: str) -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        return int(s.getsockname()[1])


def serve_directory(directory: Path, host: str, port: int) -> socketserver.TCPServer:
    handler = http.server.SimpleHTTPRequestHandler
    # Python 3.7+: handler supports `directory=` to avoid chdir
    httpd = socketserver.TCPServer((host, port), lambda *a, **kw: handler(*a, directory=str(directory), **kw))
    return httpd


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="docs", help="Directory to serve (static output folder)")
    p.add_argument("--host", default="127.0.0.1", help="Bind host")
    p.add_argument("--port", type=int, default=0, help="Port (0 = auto)")
    p.add_argument("--open", dest="do_open", action="store_true", default=True, help="Open browser (default)")
    p.add_argument("--no-open", dest="do_open", action="store_false", help="Do not open browser")
    p.add_argument("--delay", type=float, default=0.1, help="Seconds to wait before opening")
    args = p.parse_args()

    directory = Path(args.dir).resolve()
    if not directory.exists() or not directory.is_dir():
        print(f"ERROR: directory not found: {directory}")
        return 2

    port = args.port or pick_port(args.host)
    httpd = serve_directory(directory, args.host, port)

    url = f"http://{args.host}:{port}/"

    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    if args.do_open:
        time.sleep(max(0.0, args.delay))
        webbrowser.open(url, new=2)

    print(f"Serving {directory} at {url} (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
        httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
