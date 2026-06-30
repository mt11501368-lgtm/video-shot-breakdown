#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def find_binary(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    if os.name == "nt":
        fallback = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / f"{name}.exe"
        if fallback.exists():
            return str(fallback)
    raise FileNotFoundError(f"Missing required binary: {name}")


def run(command, capture=False):
    return subprocess.run(
        command,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def make_contact_sheets(frame_dir: Path, output_dir: Path, interval: float):
    frames = sorted(frame_dir.glob("ref_*.jpg"))
    if not frames:
        return []
    output_dir.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h = 480, 222
    margin, label_h, columns, rows = 6, 28, 4, 4
    sheet_paths = []
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()

    for sheet_idx in range(0, len(frames), columns * rows):
        batch = frames[sheet_idx:sheet_idx + columns * rows]
        canvas = Image.new("RGB", (columns * (tile_w + margin) + margin, rows * (tile_h + label_h + margin) + margin), "#111111")
        draw = ImageDraw.Draw(canvas)
        for local_idx, path in enumerate(batch):
            global_idx = sheet_idx + local_idx
            image = Image.open(path).convert("RGB")
            image.thumbnail((tile_w, tile_h))
            x = margin + (local_idx % columns) * (tile_w + margin)
            y = margin + (local_idx // columns) * (tile_h + label_h + margin)
            canvas.paste(image, (x, y + label_h))
            seconds = global_idx * interval
            label = f"{int(seconds // 60):02d}:{seconds % 60:04.1f}"
            draw.rectangle((x, y, x + tile_w, y + label_h), fill="#111111")
            draw.text((x + 8, y + 4), label, fill="white", font=font)
        out = output_dir / f"contact_{len(sheet_paths) + 1:02d}.jpg"
        canvas.save(out, quality=88)
        sheet_paths.append(str(out.resolve()))
    return sheet_paths


def main():
    parser = argparse.ArgumentParser(description="Probe a video and extract evidence for shot breakdown.")
    parser.add_argument("video", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--contact-interval", type=float, default=2.0)
    parser.add_argument("--scene-threshold", type=float, default=0.32)
    parser.add_argument("--skip-audio", action="store_true")
    args = parser.parse_args()

    video = args.video.expanduser().resolve()
    if not video.exists():
        raise FileNotFoundError(video)
    out = args.output_dir.expanduser().resolve()
    refs = out / "reference_frames"
    scenes = out / "scene_candidates"
    contacts = out / "contact_sheets"
    for folder in (out, refs, scenes, contacts):
        folder.mkdir(parents=True, exist_ok=True)

    ffmpeg, ffprobe = find_binary("ffmpeg"), find_binary("ffprobe")
    probe = run([
        ffprobe, "-v", "error", "-show_entries",
        "format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json", str(video),
    ], capture=True)
    metadata = json.loads(probe.stdout)
    metadata["source"] = str(video)
    (out / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    fps_filter = f"fps=1/{args.contact_interval},scale=960:-2"
    run([
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(video),
        "-vf", fps_filter, "-q:v", "3", str(refs / "ref_%04d.jpg"),
    ])
    ref_paths = sorted(refs.glob("ref_*.jpg"))
    ref_manifest = [
        {"index": i + 1, "timestamp_seconds": round(i * args.contact_interval, 3), "file": str(path.resolve())}
        for i, path in enumerate(ref_paths)
    ]
    (out / "reference_frames.json").write_text(json.dumps(ref_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    contact_paths = make_contact_sheets(refs, contacts, args.contact_interval)

    scene_filter = f"select='gt(scene,{args.scene_threshold})',showinfo,scale=1170:-2"
    scene_run = run([
        ffmpeg, "-y", "-hide_banner", "-i", str(video), "-vf", scene_filter,
        "-an", "-vsync", "0", "-q:v", "3", str(scenes / "scene_%04d.jpg"),
    ], capture=True)
    times = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", scene_run.stderr)]
    scene_paths = sorted(scenes.glob("scene_*.jpg"))
    scene_manifest = [
        {"index": i + 1, "timestamp_seconds": times[i] if i < len(times) else None, "file": str(path.resolve())}
        for i, path in enumerate(scene_paths)
    ]
    (out / "scene_candidates.json").write_text(json.dumps(scene_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    audio_path = None
    if not args.skip_audio:
        audio_path = out / "audio.wav"
        run([
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(video),
            "-vn", "-ac", "1", "-ar", "16000", str(audio_path),
        ])

    result = {
        "metadata": str((out / "metadata.json").resolve()),
        "reference_frames": len(ref_paths),
        "contact_sheets": contact_paths,
        "scene_candidates": len(scene_paths),
        "scene_manifest": str((out / "scene_candidates.json").resolve()),
        "audio": str(audio_path.resolve()) if audio_path else None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

