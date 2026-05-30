from __future__ import annotations

import argparse
from http.server import ThreadingHTTPServer

from src.webui.backend.routes import Handler
from src.webui.backend.state import state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-explain", action="store_true")
    args = parser.parse_args()

    state.load(args.config, with_explainer=not args.no_explain)
    server = ThreadingHTTPServer((args.host, args.port), Handler)

    print(f"WebUI 已启动：http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
