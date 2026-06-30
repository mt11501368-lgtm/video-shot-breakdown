# Video Shot Breakdown

[中文](#中文说明) | [English](#english)

## 中文说明

一个用于视频拉片、逐镜拆解和模仿复刻的 Codex Skill。

## 功能

- 分析 MP4、MOV、MKV、WebM 视频
- 自动提取关键帧和分镜
- 整理台词、运镜、剪辑、声音与画面信息
- 生成学习分析和模仿复刻方案
- 输出带关键帧的 Excel 工作簿

## 安装

在 PowerShell 中运行：

```powershell
git clone https://github.com/mt11501368-lgtm/video-shot-breakdown.git "$env:USERPROFILE\.codex\skills\video-shot-breakdown"
```

安装完成后重启 Codex。

## 依赖

- Python
- FFmpeg / FFprobe
- Pillow
- openpyxl
- faster-whisper（可选，用于语音转录）

检查依赖：

```powershell
python scripts/check_dependencies.py
```

## 使用示例

在 Codex 中提供一个视频文件，然后输入：

> 帮我对这个视频进行逐镜拉片，生成学习分析和模仿复刻 Excel。

## 项目结构

- `SKILL.md`：Skill 主说明
- `scripts/`：视频分析和工作簿生成脚本
- `references/`：分析规范与模式说明
- `agents/`：Codex 配置

---

## English

A Codex skill for video shot breakdown, learning analysis, and executable replication planning.

### Features

- Analyze MP4, MOV, MKV, and WebM videos
- Extract keyframes and identify narrative shots
- Organize dialogue, camera movement, editing, sound, and visual details
- Generate learning analysis and replication plans
- Export Excel workbooks with embedded keyframes

### Installation

Run the following command in PowerShell:

```powershell
git clone https://github.com/mt11501368-lgtm/video-shot-breakdown.git "$env:USERPROFILE\.codex\skills\video-shot-breakdown"
```

Restart Codex after installation.

### Requirements

- Python
- FFmpeg / FFprobe
- Pillow
- openpyxl
- faster-whisper (optional, for speech transcription)

Check the dependencies:

```powershell
python scripts/check_dependencies.py
```

### Usage Example

Attach a video file in Codex, then enter a request such as:

> Break this video down shot by shot and generate learning-analysis and replication Excel workbooks.

### Project Structure

- `SKILL.md`: Main skill instructions
- `scripts/`: Video analysis and workbook generation scripts
- `references/`: Analysis schema and mode-specific guidance
- `agents/`: Codex configuration
