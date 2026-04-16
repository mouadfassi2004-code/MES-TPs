import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from client import run_client

if __name__ == "__main__":
    run_client()