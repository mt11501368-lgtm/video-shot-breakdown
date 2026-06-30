#!/usr/bin/env python3
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path


def find_binary(name: str):
    found = shutil.which(name)
    if found:
        return str(Path(found).resolve())
    if os.name == "nt":
        fallback = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / f"{name}.exe"
        if fallback.exists():
            return str(fallback.resolve())
    return None


result = {
    "python": sys.executable,
    "ffmpeg": find_binary("ffmpeg"),
    "ffprobe": find_binary("ffprobe"),
    "modules": {
        "openpyxl": bool(importlib.util.find_spec("openpyxl")),
        "PIL": bool(importlib.util.find_spec("PIL")),
        "faster_whisper": bool(importlib.util.find_spec("faster_whisper")),
    },
}
required_ok = bool(result["ffmpeg"] and result["ffprobe"] and result["modules"]["openpyxl"] and result["modules"]["PIL"])
result["required_ok"] = required_ok
result["transcription_available"] = result["modules"]["faster_whisper"]
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if required_ok else 1)

