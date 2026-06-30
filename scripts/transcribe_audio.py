#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Transcribe extracted audio with faster-whisper.")
    parser.add_argument("audio", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    args = parser.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit("faster-whisper is not installed. Obtain user approval before installing packages or downloading a model.") from exc

    audio = args.audio.expanduser().resolve()
    if not audio.exists():
        raise FileNotFoundError(audio)
    out = args.output_dir.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(
        str(audio), language=args.language, beam_size=5, vad_filter=True, condition_on_previous_text=True,
    )
    rows = []
    for segment in segments:
        text = segment.text.strip()
        if text:
            rows.append({"start": round(segment.start, 3), "end": round(segment.end, 3), "text": text})

    payload = {
        "audio": str(audio),
        "language": info.language,
        "language_probability": info.language_probability,
        "segments": rows,
    }
    json_path = out / "transcript.json"
    text_path = out / "transcript.txt"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    text_path.write_text("\n".join(f"[{r['start']:06.2f} --> {r['end']:06.2f}] {r['text']}" for r in rows) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(json_path), "text": str(text_path), "segments": len(rows)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

