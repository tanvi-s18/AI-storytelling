import json
import os
from config import OUTPUT_DIR


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_text(filename: str, text: str):
    ensure_output_dir()
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(text)


def save_json(filename: str, obj):
    ensure_output_dir()
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)