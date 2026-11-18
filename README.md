# 视频创作 / Video Creation

维护视频 ideas、原创研究、制作方法与可验证进展。页面入口为 [视频创作](https://farmcan.pages.dev/creation/)，使用既有 farmcan 站点；普通创作资料免登录，原媒体与账号资料不发布。

## 后续 Agent 从这里开始

1. [通用创作方法](docs/creative-song-workflow.md)：按既有旋律写新词，从标杆研究、立意和梗，到乐句约束、自然英语、生产与验收。附来源、采用程度和可复制模板；适用于换人物或主题。
2. [录音方案](docs/audio-recording.md)：本机已走通的系统声回环、短测、全曲录制、恢复设置及检查方法。
3. [黄仁勋题材案例](projects/jensen-song-2026-11-17/README.md)：当前词稿、研究、实际制作与历史失败入口；[本地素材索引](projects/jensen-song-2026-11-17/LOCAL-ASSETS.md)说明录音和参考在哪里。

完整索引见 [docs/README.md](docs/README.md)。先读通用方法，再读目标项目；别把某次平台参数、热点事实或旧完成记录当成长期规则。

## 当前进展 · 2026-11-18

黄仁勋题材的 [英文 v2](projects/jensen-song-2026-11-17/lyrics-en-v2.txt)与[中文梗说明](projects/jensen-song-2026-11-17/SONG-v2.md)已保留。Suno 生成 A／B 两首候选；A 已完成约 4:12 的本地播放录制，三份音频大小与哈希核对通过，连续性检查没有发现曲内持续半秒以上的静音。原曲逐句旋律、实际唱词细节与最终听感仍待验，B 尚无同等完整录制验收。

旧会话「查看音乐生成参考」在音频工具结果引入 `input_audio` 后连续返回 HTTP 400；在新会话通过文档与文件接续，未宣称旧会话已经修复。剪映导入的准备与边界见 [导入说明](docs/jianying-import.md)。

## 目录与维护

| 目录 | 保存内容 |
| --- | --- |
| `docs/` | 跨题材工作流、录音与交接说明 |
| `research/` | 原创方法研究、带日期的来源／许可快照 |
| `projects/` | 栏目状态与单个作品的立意、词稿、输入、运行和验收 |
| `scripts/` | Python 静态构建与显式导出 |
| `site/` | 页面模板、样式和原创图标 |
| `dist/` | 忽略提交的生成页面 |

只在 main 维护。v1 是失败请求的真实输入，v2 是当前认可词稿，两者保留便于追溯；不删掉研究来源、许可或失败原因。音轨、完整第三方词稿、截图、账号信息和完整诊断日志放仓库外，原媒体扩展名已忽略提交。

## 构建与发布

需要 Python 3，无第三方构建依赖。

```sh
python3 scripts/build.py
python3 scripts/export.py --target ../farmcan-websites
```

先检查链接、隐私和构建，提交并推送本仓库；再显式导出选定静态文件到 farmcan-websites 的 `site/creation/` 并推 main。复用既有 Actions，核对 release.json、首页和 creation 文件哈希；不新建 Cloudflare 项目。文档和素材目录不随静态包整体导出。

源码、界面与原创文档使用 MIT；引用工具、词典及外部作品保留各自许可和权利。研究、页面可用、音频连续性、词曲合格与公开发布分别验收。
