# 本次本地素材与接续入口

核对日期：2026-11-18。`~` 指本机用户目录；以下文件只在本地，不随 Git 发布。原会话是「查看音乐生成参考」（`01a1e9e5-6dd1-70e1-b5f9-c15ace6b32bc`），后续 agent 先读 [PLAN](PLAN.md)、[v2 词稿](SONG-v2.md)、[分句表](PHRASING-v2.md)、[播放验收](PLAYBACK-QA-20261118.md)，再按需要打开素材。通用录音流程见 [audio-recording](../../docs/audio-recording.md)。

## A 版完整录音（已核实存在）

目录：`~/Movies/AI-Music/2026-11-18-jensen/`。

| 文件 | 用途／已核状态 |
| --- | --- |
| `let-him-cook-take-a-full.mp3` | 约 252.50 秒、4:12 兼容试听版；6,062,013 bytes。 |
| `let-him-cook-take-a-full.m4a` | 约 252.50 秒、裁首尾空白后的试听版；10,249,025 bytes。 |
| `take-a-recording-raw.m4a` | 约 275.294 秒 QuickTime 原录音；10,259,886 bytes，保留不覆盖。 |
| `recording-info.json` | 来源链接、v2、时长、裁剪参数、文件 SHA-256、恢复输出及验收边界。 |
| `take-a-recording-audit.json` | 录音连续性／电平的本地数字审计。 |
| `take-a-local-asr-unprompted.txt` / `.json` | 无目标歌词提示的 tiny English 转写；辅助定位，非可靠最终歌词。 |

上述三份音频已逐一核对大小与 SHA-256，均匹配 `recording-info.json`。原播放时长 251.96 秒；裁剪从原录音 1.5 秒开始、保留约 252.5 秒。20 ms RMS 检查中，曲内没有持续至少 0.5 秒且低于 -60 dBFS 的静音段；这只通过录音连续性。

来源：[Suno A](https://suno.com/song/9cdfd5ff-2714-499f-9890-5232fd11c634)。B 为 [4:27 候选](https://suno.com/song/c04c06d7-34c3-46a3-b6fd-82b7acee54f1)，尚无完整本地录音验收。链接存在于历史实跑记录，不保证以后账号／页面仍可访问。

## 原曲与参考（已核实存在）

目录：`~/wrksp/seed/library/research/ai-music-benchmark-2026-10-19/`。

| 文件 | 用途／边界 |
| --- | --- |
| `source_chinese_original_candidate.m4a` | 原中文 MV 候选的本地音轨；版本与权属边界见 REFERENCE-STUDY。 |
| `reference_english_target.m4a` | 华尔街英语改词参考的本地音轨；用于结构、反讽和词曲研究。 |
| `source_chinese_original_candidate.source.json` / `reference_english_target.source.json` | 原缓存来源元数据；仅按需要本地读取。 |

本项目只公开原创机制分析：[REFERENCE-STUDY](REFERENCE-STUDY.md)。原音轨、完整第三方歌词、字幕截图不复制进本仓库。

## 临时工具与诊断

`~/.codex/tmp/music-methods-20261117/` 内已有 `audit_audio.py`、`check_lyrics.py`、`compare_melody.py`、27 秒诊断片段、模型与临时环境。临时路径可能被清理；持久接续以本项目文档和 Movies 目录为准。临时脚本存在不代表其结论已验收；尤其旋律比较结果不能替代逐句原主旋律核对。

原会话日志：`~/.codex/sessions/2026/11/17/rollout-2026-11-17T22-24-49-01a1e9e5-6dd1-70e1-b5f9-c15ace6b32bc.jsonl`。仅排错时窄读相关事件，勿复制音频 base64、账号资料或完整日志到公开仓库。

## 下一步验收

A 已通过完整有声录制和连续性；目标唱词在多个段落被辅助识别。仍需核对主歌、各遍副歌尤其最终副歌的原旋律、自然重音和实际唱词，再判断听感与是否选 A。当前保留用户重新阅读后认可的 v2，不因 ASR 不稳或后备梗思路自动重写。
