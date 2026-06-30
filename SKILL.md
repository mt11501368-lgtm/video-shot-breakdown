---
name: video-shot-breakdown
description: Analyze video files into shot-by-shot breakdowns and Excel workbooks for learning analysis or executable imitation and replication. Use when Codex is asked for 视频拉片、逐镜拆解、学习拆解、模仿复刻、分镜脚本、拍摄清单、台词文案、剪辑时间轴、关键帧提取、AI 视频提示词，或需要分析 .mp4、.mov、.mkv、.webm 等视频文件。
---

# Video Shot Breakdown

Turn a supplied video into evidence-backed shot analysis and production-ready Excel workbooks. Support two modes:

- **Learning analysis**: answer why the video works and extract transferable principles.
- **Imitation/replication**: answer how to produce a similar result with an executable plan.

## Workflow

1. Confirm the video path and requested mode. Default to `both` when the user asks for a complete breakdown.
2. Check local requirements:

   ```powershell
   python scripts/check_dependencies.py
   ```

3. Probe the video and extract reference frames, contact sheets, scene candidates, and audio:

   ```powershell
   python scripts/probe_extract.py VIDEO --output-dir OUTPUT_DIR
   ```

4. Inspect every contact sheet. Treat automatic scene candidates only as hints. Merge AI morphs, flashes, camera shakes, and same-action microcuts into executable narrative shots.
5. If accurate dialogue matters, transcribe the extracted audio:

   ```powershell
   python scripts/transcribe_audio.py OUTPUT_DIR/audio.wav --output-dir OUTPUT_DIR/transcript
   ```

   Cross-check the transcript against visible subtitles. Mark uncertain lines instead of inventing words.
6. Build the analysis JSON described in [references/analysis-schema.md](references/analysis-schema.md). Use one representative keyframe per narrative shot.
7. Read the mode-specific guidance:
   - Learning analysis: [references/learning-mode.md](references/learning-mode.md)
   - Imitation/replication: [references/replica-mode.md](references/replica-mode.md)
8. Generate Excel workbooks:

   ```powershell
   python scripts/build_workbooks.py analysis.json --mode both --output-dir OUTPUT_DIR
   ```

9. Open the generated files programmatically and verify sheet names, row counts, and embedded-image counts before delivery.

## Shot Grouping Rules

- Split when subject, location, camera setup, narrative function, or action beat materially changes.
- Keep a continuous camera move as one shot even if the image morphs internally.
- Merge rapid inserts when they express one inseparable action beat; split them when each insert has a distinct setup, impact, or reaction.
- Preserve exact timecodes to the nearest practical tenth of a second.
- Distinguish observed facts from inferred intent. Phrase uncertain audio or motivation as an inference.

## Output Requirements

- Embed keyframes directly in the main Excel table.
- Freeze headers, enable filters, wrap text, use readable column widths, and validate the workbook after saving.
- Keep analysis specific to the supplied video. Do not fill cells with generic film-school definitions.
- For AI prompts, describe subject, action, environment, framing, camera movement, light, mood, and continuity anchors.
- For replication, make every row executable: what to shoot, duration, actor blocking, camera, edit point, dialogue, and sound.
- Return clickable links to the generated files and state what each workbook contains.

## Dependencies and Fallbacks

- Require FFmpeg/FFprobe, Python, Pillow, and openpyxl.
- Treat faster-whisper as optional. Ask before installing packages or downloading a model when authorization is required.
- If transcription is unavailable, rely on visible subtitles and explicitly label uncertain dialogue.
- If scene detection is noisy, prioritize fixed-interval contact sheets and manual narrative grouping.

