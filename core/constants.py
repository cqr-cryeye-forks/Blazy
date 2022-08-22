from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
OUTPUT_FILE = 'output.json'
BASE_OUTPUT_PATH = BASE_DIR.joinpath(OUTPUT_FILE)
