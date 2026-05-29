from __future__ import annotations

import argparse
import threading
from http.server import ThreadingHTTPServer

from src.webui.backend.routes import Handler
from src.webui.backend.state import state
from src.webui.frontend.api import BackendClient
from src.webui.frontend.interface import create_interface


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-explain", action="store_true")
    args = parser.parse_args()

    state.load(args.config, with_explainer=not args.no_explain)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    backend_url = f"http://{args.host}:{args.port}"
    create_interface(BackendClient(backend_url)).launch()


if __name__ == "__main__":
    main()

