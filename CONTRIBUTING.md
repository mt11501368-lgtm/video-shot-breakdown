# Contributing

感谢你改进 Video Shot Breakdown。

## 开始前

1. Fork 仓库并从 `main` 创建分支。
2. 保持修改范围清晰；一个 Pull Request 尽量只解决一个问题。
3. 不要提交视频、音频、模型文件、转录缓存或生成的工作簿。
4. 如果修改分析字段，请同步更新 `references/analysis-schema.md` 和相关脚本。

## 本地检查

```powershell
python scripts/check_dependencies.py
python scripts/probe_extract.py --help
python scripts/transcribe_audio.py --help
python scripts/build_workbooks.py --help
```

如果修改了工作簿生成逻辑，请用一个短测试视频生成文件，并确认：

- 工作表名称正确
- 行数符合分析 JSON
- 关键帧成功嵌入
- 表头冻结、筛选和自动换行仍然有效

## 提交 Issue

请提供操作系统、Python 与 FFmpeg 版本、执行命令、完整错误信息，以及能复现问题的最小步骤。分享视频前请确认你拥有相应权限。

## English

Fork the repository, create a focused branch from `main`, and keep each pull request limited to one clear change. Do not commit videos, audio, model files, transcript caches, or generated workbooks. If you change analysis fields, update both `references/analysis-schema.md` and the affected scripts.

Run the local checks above before opening a pull request. For workbook changes, verify sheet names, row counts, embedded keyframes, frozen headers, filters, and wrapping.
