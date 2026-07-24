import argparse
import os

import uvicorn


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["test", "prod"], default="test")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    os.environ["TEAINE_RULER_ENV"] = args.env
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=False)
