# 剪映成片工作流调研

观察日期：2026-11-18，Asia/Shanghai。用户明确后续使用剪映成片；本轮先研究参考素材与现成工具，再在本机准备音轨和可编辑歌词。本文记录调研与可执行方案；主执行者已实测音轨入时间线，字幕导入与完整成片导出仍按后续记录验收。

## 这次最短可行路径

**先用已经安装的 Mac 剪映 GUI：新建本地工程 → 导入持久 MP3 → 导入 UTF-8 SRT → 检查首段／各遍副歌 → 退出工程并重新打开 → 导出一个短片验证。** 当前不需要先安装一整套剪辑框架。SRT 文件、原始英文词稿和中文改写一起保存；以后 Agent 可以先准备数据，再在同一工程精修画面。

本机只读核验发现 `/Applications/VideoFusion-macOS.app`：Info.plist 的 bundle ID 为 `com.lemon.lvpro`，版本 `10.7.0`，Spotlight 也返回同一路径。旧文 [jianying-import.md](jianying-import.md) 中按“剪映／CapCut”文件名查找而判断没有应用，存在漏检；本次已定位入口，但尚未由本调研者打开 UI。后续按 bundle ID／真实界面识别，不只看 `.app` 文件名。

同日主执行者的实际界面回执：文件 → 新建草稿；Cmd+I 导入 Movies 中完整 MP3；素材右键 → 根据选中素材新建时间线，音频从 0 开始、覆盖约 4:12。字幕入口已实际见到“字幕 → 新建字幕 → 导入本地字幕”，选择器列 SRT／LRC／ASS。这比国际版文档更贴近本机，但仍需以文件真正进入时间线和保存重开验证字幕导入成功。普通拖拽和 `e` 快捷键本轮未见效果，不列为本机已验路径。

用户否决了直接生成的通用插画，要求先找热度较高的真实梗图、短片、视觉风格和方法论。剪映工程可先放音轨与字幕；不要把被否决的三张试图当作已批准视觉母版继续铺满全曲。

## 官方入口与格式边界

在剪映／CapCut 官方域名及 ByteDance GitHub 定向检索中，本轮未找到可核实、可直接用于本机草稿编辑的官方 agent skill 或官方桌面自动化 API。这个结论是检索覆盖边界，不是证明官方永远没有相关能力。第三方项目不能冠以“官方”。

[CapCut 官方导入说明](https://www.capcut.com/help/how-to-import-subtitles)区分了桌面端的 SRT／带时间码 TXT 与网页端的 SRT。导入后的对象可继续修改；UTF-8、合法起止时间和分段格式是基本要求。该文描述国际版，不能直接证明中国版剪映 10.7.0 的菜单位置；实际入口需在本机观察。

**普通歌词 TXT 是文稿，不等于同步字幕。** 无时间码文本不能保证自动填到对应唱词位置。歌词识别、文稿匹配或歌曲自动字幕是否可用、支持何种语言、是否消耗会员额度，须看本机当前界面；这次优先导入本地 SRT，不把平台 AI 识别列为前提。

## GitHub 候选与实际代码核查

星数、push 时间为本轮 GitHub API 快照，不代表兼容性或质量；所有工具均未在本机安装／运行。

| 项目／快照 | 看过什么 | 对本机任务的判断 |
| --- | --- | --- |
| [isYangs/jianying-editor-skill](https://github.com/isYangs/jianying-editor-skill/tree/b7225641d39a9cd354ec265e2f6101b009fa1b44)，471 星，MIT，2026-10-15 push | README、SKILL、requirements、`scripts/jy_wrapper.py`、`auto_exporter.py`。wrapper 存在 macOS 分支和草稿路径处理，但 Mac 导出走手动指南／Windows 代理；requirements 无条件列 `uiautomation` 等依赖。 | 可研究其封装方式，不能把“Mac 支持”理解成本机全自动成片。当前先 GUI 导入，省去跨机代理与旧版导出条件。 |
| [GuanYixuan/pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft/tree/1e228479dda361e312e85f6037002346cf6dca9a)，4,931 星，Apache-2.0，2026-10-14 push | README、setup、`draft_folder.py`、`_script_file_segments.py`、controller 和字幕测试。`import_srt` 读取 UTF-8-SIG，逐条建立原生文字；新建草稿默认禁止覆盖同名项目。 | 适合作为数据／草稿表示的参考。作者仍将跨平台生成与 Windows 原生导出分开；不能据其新版 Windows 测试表推断本机 Mac 10.7 已通过。 |
| [GuanYixuan/pyCapCut](https://github.com/GuanYixuan/pyCapCut/tree/ec61408d9f039c4045f946370bb35746b89b2479)，758 星，API 未识别许可，2026-10-16 push | README。面向 CapCut，文档同样要求 Windows 版打开／导出；提示接口有迁移。 | 与中国版剪映不是同一目标；本轮不采用，也不把 API 的空许可字段解释成无版权。 |
| [Capricornus-joe/jianying-local-mcp](https://github.com/Capricornus-joe/jianying-local-mcp/tree/f47f907e7bc15e68082238e50ca5964c50b2f559)，14 星，MIT，2026-09-18 push | README、pyproject、兼容性说明，以及字幕／发布／server 源码入口。明确面向 Mac，提供新管理工程、SRT 与原生草稿登记。 | 低星但目标更贴近本机，可作后备。作者历史样片版本为 Mac 剪映 11.4.0，与本机 10.7.0 不同；仍需本机小工程验证。没有 Mac 自动导出，也不回写 GUI 的修改。 |

`pyJianYingDraft` 具体证据：[SRT 实现](https://github.com/GuanYixuan/pyJianYingDraft/blob/1e228479dda361e312e85f6037002346cf6dca9a/pyJianYingDraft/_script_file_segments.py)、[草稿创建／复制](https://github.com/GuanYixuan/pyJianYingDraft/blob/1e228479dda361e312e85f6037002346cf6dca9a/pyJianYingDraft/draft_folder.py)、[Windows UI 导出 controller](https://github.com/GuanYixuan/pyJianYingDraft/blob/1e228479dda361e312e85f6037002346cf6dca9a/pyJianYingDraft/jianying_controller.py)。这些是代码阅读，不是本机功能实测。

Mac 后备工具的[兼容性合同](https://github.com/Capricornus-joe/jianying-local-mcp/blob/f47f907e7bc15e68082238e50ca5964c50b2f559/docs/compatibility.md)将程序测试、历史原生样片与新版接口验收分开，值得复用其验证方法。它不支持任意加密草稿回读；也不保证手工改过的工程能再由管理计划无损重建。本次不借调研启用这些能力。

## 本次歌词工程的准备与导入

1. **固定素材。** 用 [本地索引](../projects/jensen-song-2026-11-17/LOCAL-ASSETS.md) 中 Movies 目录的完整 A 版 MP3；保留约 252.50 秒的文件、哈希和源录音。正常英文稿用 `lyrics-en-v2.txt`，不用带发音改写的 Suno 输入稿充当字幕。中文 `lyrics-zh-v1.txt` 是改写稿，和英文目标分别保留。
2. **生成可检查的 SRT。** 顺序号、`HH:MM:SS,mmm --> HH:MM:SS,mmm`、正文、空行；结束晚于开始且不越过音轨时长。可把中英两行放同一 cue，也可导入两份 SRT 形成独立轨道，实际取决于本机能否方便选中和批改。不按字数平均分摊整首时间。
3. **时间与正文分开核。** 既有无提示 ASR 只提供段落锚点，姓名、缩写和唱词有误识别。SRT 正文来自目标词稿，时间初稿须标待校；不能把这种文件称作逐字真实演唱转录。后续按主歌、三遍副歌和尾奏逐段回听修正。
4. **建立原生工程。** 新建独立名称，例如 `Let Him Cook — A — captions-v1`，导入 MP3 并放在音频轨起点。记录应用版本、项目名、实际草稿位置和画幅。此时可以先不放未批准画面。
5. **导入和检查文字。** 在实际 UI 找到“文本／字幕 → 本地字幕／导入字幕”；按钮名以本机为准。导入 SRT，观察时间轴上有多个可选中文字片段；抽查开头、每遍副歌、最后一句，确认中英文、换行、字体和标点。
6. **验证保存。** 返回首页，重新进入同名工程；确认音轨和字幕还在、路径不丢、时长合理，修改一条文字再重开，证明可编辑对象真正保存。保存成功与视频导出成功分别记录。
7. **短导出闭环。** 后续加合法参考素材后先导出一个覆盖首句、包袱和收尾的短段，验证画面、声音、字幕与编码，再铺全曲。剪映成片目标不由外部 FFmpeg 试片替代。

歌词填入、时间粗对齐、逐句听辨、视觉通过和最终导出是不同阶段。UI 导入失败时先保留同一工程，检查文件编码／格式与实际入口；有界重试后再评估 Mac 草稿后备工具，避免同时安装多个框架或覆盖已有工程。

## 后续 Agent 的交接合同

每个作品保留：创作范围与版本、参考素材来源和可用状态、项目名／应用版本、素材目录与相对关系、原始词稿、SRT 文件／条数／时长／哈希、时间校对状态、抽查位置、草稿重开结果、导出文件参数与视听问题。媒体、账号、完整诊断与第三方截图留私有本地；公开仓库只存原创方法、脱敏状态和来源链接。

未来批量化的停止条件：未能在本机打开、修改字幕、重开保留、导出并视听检查前，不把任何第三方生成器列为已接入；不要因 JSON 写成功、测试数量多或作者截图存在就扩大到全曲生产。

## 本次可直接导入的字幕草稿

标准库入口 [prepare_jianying_subtitles.py](../scripts/prepare_jianying_subtitles.py) 将当前英文 v2、中文改写 v1 的 44 行与已有无提示 ASR token 时间做单调模糊词对齐；没有启动新 ASR 或费用。输出保存在本机私有目录 `~/Movies/AI-Music/2026-11-18-jensen/jianying-import/`：

- `lyrics-bilingual-draft.srt`：44 个英文／中文双行 cue，含四处呼应和完整三遍副歌，时码无重叠，32.77–236.92 秒。
- `lyrics-bilingual-draft.cues.json`：源文件哈希、逐词锚点、覆盖率、局部插值与低置信标记。

第 6 句 Prime-time 和第 21 句 Everyone's a PhD 缺少足够锚点，只在邻句之间局部插值；没有整首均摊时间。低置信 cue 为 2、6、10、12、15、17、19、21、28、33、41。全部 cue 都保留听辨细校状态；正文是目标词，不是已核实实际演唱转录。脚本默认拒绝覆盖已有输出，重做请指定新的输出目录。

## v1 播放失败与 v2 候选更正

用户实际观看指出字幕比音频快、持续太短，故上述 v1 的时间方案已被证伪；文件结构与时码检查通过不等于同步通过。第 12 句名字与回归句被裁成 82.62–83.93 秒，仅 1.31 秒；原因是以“匹配到的单词包围框”代替完整乐句，姓名识别错误又漏掉句首。重新处理实际音频后还发现，旧全曲 ASR 把第一遍副歌开头放在 75.26 秒，而新分段识别约为 79.30 秒；不能只给旧字幕延长尾部。

本轮重新用已有 tiny.en-q5_1 对原音轨及第一主歌、第二主歌、第一副歌、后两遍副歌的实际音频做无歌词提示的本地识别。`whisper-cli -dtw tiny.en` 会在默认 flash attention 下自动禁用 DTW；必须加 `-nfa`，检查日志 `dtw=1` 和非负 `t_dtw`，才把它记作实际 DTW 运行。第一次副歌约 3 秒、全曲约 12 秒完成；全部运行均未调用付费服务或向会话注入音频。尝试官方 whisper.cpp 指定 Hugging Face 源的 small.en 下载，首次 TLS 失败、一次 Python TLS 重试约 166 秒超时，未取得模型，不声称使用了 small.en。

新的 [v2 组装入口](../scripts/prepare_jianying_subtitles_v2.py) 按分段实际识别的完整乐句和下一句入口组合字幕，并留间奏／尾奏空白。本机同一 `jianying-import/` 目录已输出：

- `lyrics-bilingual-v2.srt`：44 cue，32.90–237.96 秒；第一遍副歌约 79.30–111.36 秒。
- `lyrics-bilingual-v2.diagnosis.json`：逐句 v1／v2 起止与持续时间、来源窗口、组装理由和实际 ASR／DTW 证据哈希。
- `lyrics-bilingual-chorus-v2.srt`：仅第一遍副歌八句，保留完整音轨的绝对时间，供先验证关键段落。

八句副歌的显示覆盖总时长从 27.11 秒增至 31.78 秒，名字句从 1.31 秒增至 3.78 秒；Prime-time 与 PhD 在新的局部识别中已被恢复。上述是基于真实文件重跑的修订证据，**仍只算 v2 候选，尚未获得用户原生播放接受或逐句听辨通过**。不要把更长时长、有效 DTW 或正确格式直接写成“已经对齐”。旧 v1 文件原样保留，作为失败样本，不再推荐导入新工程。

## 仓库内可复用文件与防误用

[captions/manifest.json](../projects/jensen-song-2026-11-17/captions/manifest.json) 保留两版状态：v1 的 SRT 字节原样保留，标为 `failed_timing`；v2 是当前候选，导入、重开、用户时序接受和导出各自记录，不相互替代。仓库现有 [完整 v2 SRT](../projects/jensen-song-2026-11-17/captions/lyrics-bilingual-v2.srt)、[副歌验证版](../projects/jensen-song-2026-11-17/captions/lyrics-bilingual-chorus-v2.srt)与[脱敏时序诊断](../projects/jensen-song-2026-11-17/captions/lyrics-bilingual-v2.diagnosis.json)。公开诊断只含目标歌词、时码、方法、哈希和失败边界，原 ASR、音轨、运行日志与截图不复制。

旧 `prepare_jianying_subtitles.py` 默认拒绝执行；仅显式加 `--reproduce-failed-v1` 才能复现失败方案。v2 组装脚本必须给新的 `--output` 目录，而且 SRT／诊断任一已存在就拒绝覆盖。例如，使用一个尚不存在的目录名：

```sh
python3 scripts/prepare_jianying_subtitles_v2.py --output local/subtitle-v2-rebuild-01
python3 scripts/check_jianying_subtitles.py
```

检查器验证 44 句目标内容、三遍副歌、四处呼应、时码递增、非重叠、最低显示长度、SRT／诊断／源词稿哈希一致和脱敏边界。它不检查真实唱词同步；用户原生播放接受仍是独立验收。
