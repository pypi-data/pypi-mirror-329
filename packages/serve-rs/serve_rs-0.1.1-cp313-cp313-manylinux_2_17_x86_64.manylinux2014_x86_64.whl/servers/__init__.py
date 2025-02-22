from .servers import start
from pathlib import Path
import argparse
import sys


def serve():
    sys.path.insert(0, str(Path.cwd()))
    parser = argparse.ArgumentParser(description="Start the server.")
    parser.add_argument("path", type=str, help="Path to the server directory")
    args = parser.parse_args()
    sys.exit(start(args.path))
