import argparse
import os

import uvicorn


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["test", "prod"], default="test")
    return parser.parse_args()


def inject_env(env: str) -> None:
    os.environ["TEAINE_RULER_ENV"] = env


def main() -> None:
    args = parse_args()
    inject_env(args.env)
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
