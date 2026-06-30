# Analysis JSON schema

Use UTF-8 JSON. Paths may be absolute or relative to the JSON file.

## Top level

```json
{
  "video": {
    "title": "Example",
    "source": "C:/path/video.mp4",
    "duration": "86.24 秒",
    "resolution": "2340×1080",
    "fps": "30fps",
    "type": "AI 国风武侠短剧"
  },
  "shots": [],
  "structure": [],
  "techniques": [],
  "checklist": [],
  "dialogue": [],
  "timeline": []
}
```

## `shots`

Create one item per narrative shot. `keyframe` is required for image embedding; other fields may be empty only when truly unavailable.

```json
{
  "no": "01",
  "start": "00:00.0",
  "end": "00:05.6",
  "keyframe": "keyframes/M01.jpg",
  "shot_size": "双人近景",
  "camera": "极慢推近",
  "visual": "Two characters whisper at a tavern table.",
  "narrative_role": "成果钩子 / 任务线建立",
  "why_effective": "Start with a result to create an information gap.",
  "emotion": "好奇 → 不安",
  "sound": "低强度悬疑底乐，对白居前",
  "transferable_formula": "异常结果 → 补充原因 → 威胁进入",
  "ai_prompt": "古代酒馆，两位女侠低声密谈……",
  "action": "Actor blocking and prop action.",
  "edit": "Cut point and transition instructions.",
  "dialogue": "角色：台词"
}
```

The workbook script calculates duration from `start` and `end`.

## `structure`

```json
{
  "shot_range": "01–04",
  "time_range": "00:00–00:14.7",
  "task": "秘密与罪行铺垫",
  "emotion": "好奇 → 愤怒 → 不安",
  "sound": "低强度悬疑底乐",
  "formula": "结果先行 → 罪行升级 → 威胁入画"
}
```

## `techniques`

```json
{
  "category": "悬念",
  "name": "危险先出现在背景",
  "evidence": "反派在主角身后逐步靠近。",
  "formula": "前景正常活动 + 背景威胁变大"
}
```

## `checklist`

```json
{
  "category": "场景",
  "item": "酒馆内景",
  "details": "木桌、格窗、门口亮区。",
  "shots": "01–15"
}
```

## `dialogue`

```json
{
  "time_range": "00:00–00:05.6",
  "shot": "01",
  "speaker": "斗笠女",
  "line": "那狗官的印记到手了。",
  "delivery": "压低声音",
  "subtitle": "居中偏下，不超过两行"
}
```

## `timeline`

```json
{
  "time_range": "00:00–00:14.7",
  "video": "镜 01–04：秘密与罪行铺垫",
  "dialogue": "Key dialogue for the segment",
  "sound": "Music and SFX plan",
  "emotion": "好奇 → 不安",
  "transition": "How to enter and leave the segment",
  "completion": "Observable completion standard"
}
```

