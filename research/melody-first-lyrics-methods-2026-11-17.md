# 有曲之后怎样写英文歌词：GitHub、论文与创作方法研究

观察日期：2026-11-17，Asia/Shanghai。任务是沿完整《朋友的酒》旋律写新的英文歌词，主题为黄仁勋事件，要求有立场、有梗且唱得进去。用户明确要求先研究方法，不能跳过研究直接作词。本文件是原创归纳；第三方完整歌词、视频、截图不存入本仓库。当前未运行这些模型，未完成词曲或听感验收。

## 结论与选择

优先组合：**SongMASS 的乐句／词曲对齐表示 + REFFLY 的保留语义、逐句改写 + 英文 prosody 检查 + Suno 的音频执行与局部修补**。这是一套据来源整理的工作流程，并非声称已经部署了这些模型或复现了论文效果。

不能只告诉通用模型“按《朋友的酒》写首英文歌”。歌名没有提供具体版本的每句起止、音节位置、强弱重音与拖音。也不能先写一首自由诗，再期待 Suno 自动恢复完整原曲。完整作品范围与小段技术试验分开：全曲歌词、段落、重复段都要交付，小段只用于定位唱法问题。

## GitHub 候选：优先高星，但按任务匹配排序

精确元数据见 [抓取快照](music-methods-github-snapshot-2026-11-17.json)。星数为当日 GitHub API 观察，不表示质量、推理成功率或单个子项目的星数。

| 项目 | 星数 | 与本任务的关系 | 本轮查到的限制与取舍 |
| --- | ---: | --- | --- |
| [Microsoft Muzic / SongMASS](https://github.com/microsoft/muzic/tree/2b8739671ba06f819f31f568b8a79da581aaf6f9/songmass) | 4,960（父仓库） | 直接相关：已有旋律生成歌词；有实际推理脚本 | 深读 README、infer_lyric.sh 和数据解析代码。需要符号旋律、词／句边界及模型环境；不是 MP3 即插即用。 |
| [Muzic / ReLyMe](https://github.com/microsoft/muzic/tree/2b8739671ba06f819f31f568b8a79da581aaf6f9/relyme) | 同一父仓库，不另计 | 可借鉴：节奏、音调、结构关系检查 | 主方向是词→曲；不能说它本身是英文按曲填词产品。Readme.md 中 SongMASS 集成小节仍写 TBD；英文评分需要 MIDI、结构和音节文件。 |
| [SongComposer](https://github.com/pjlab-songcomposer/songcomposer/tree/86c1deec706aaa9195dde8bf4fbc107c6a6b21c2) | 249 | 直接相关：melody-to-lyric，支持中英文及全曲研究 | 深读 README 与 inference.ipynb，确有旋律→词示例；旋律以音高、时值等结构化输入。PyTorch／CUDA 推理和模型权重另需准备；本机未跑。 |
| [claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills/tree/01463d350e9ff1534bdd30ce266183b6059ff075) | 672 | 实用写词／Suno 制作流程，主题研究、咬字、韵律、返工都有材料 | 深读 lyric-writer、craft-reference、Suno practices／sliders／pronunciation。没有自动读入整首曲谱并硬约束每个落字的证明。CC0-1.0；本轮仅研究，没有安装整个插件。 |
| [melodic-software songwriting](https://github.com/melodic-software/claude-code-plugins/tree/3ed61a3467fee60d2b81a3a41357ea5009fadd53/plugins/songwriting) | 32（父仓库） | 低星但题目贴切：prosody、行长、重音、收束 | 读到 prosody.md；其中大量书籍摘录不复制。用 Berklee／作者本人公开材料交叉验证。MIT 是仓库元数据，不代表可重新发布书籍引文。 |
| [suno-songwriting-skill](https://github.com/NuNaught/suno-songwriting-skill/tree/60bee7890895b05ae8693e1d32c7f9759b27389d) | 33 | 写词、保留韵律的改写、可唱性本地化与分开的 Lyrics／Style 输出 | 深读 README 与入口文件。更偏写作提示流程，不是旋律对齐算法；没有采用其逐项确认流程，也没有安装。Apache-2.0。 |
| [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) | 14,884 | 音乐生成／编辑候选，不能替代作词方法 | 本轮核元数据，继承已有研究；先前本地生成路线已经停止，未因高星重启。MIT 元数据。 |
| [YuE](https://github.com/multimodal-art-projection/YuE) | 13,558 | 歌词→歌曲的相邻路线 | 本轮核元数据；不能由整曲生成能力推断锁定《朋友的酒》全曲旋律。Apache-2.0 元数据。 |
| [Basic Pitch](https://github.com/spotify/basic-pitch) | 6,087 | 提取旋律／MIDI 的辅助候选 | 本轮核元数据，未提取本曲；自动转 MIDI 需另验漏音、滑音及伴奏干扰。Apache-2.0。 |
| [DiffSinger](https://github.com/openvpi/DiffSinger) | 3,246 | 有音符与歌词后的歌声合成候选 | 本轮核元数据；作用在唱出来，不是选择梗和写出好词。Apache-2.0 元数据；音源模型另核。 |
| [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) | 1,918 | 已有唱词／音频的对齐辅助候选 | 本轮核元数据，未验证歌唱对齐；不能把 ASR／强制对齐当旋律与重音验收。MIT。 |
| [phonemizer](https://github.com/bootphon/phonemizer) | 1,581 | 英文音素分析辅助 | 本轮核元数据；GPL-3.0，后端词典和语言规则另核；无需为此研究整套安装。 |
| [CMUdict](https://github.com/cmusphinx/cmudict) | 833 | 英语词音节与词重音的词典候选 | 本轮核元数据；API 许可证识别为 NOASSERTION，不等于无版权。姓名、品牌、缩写仍需人工核音。 |
| [Amazon melody-to-lyrics](https://github.com/amazon-science/unsupervised-melody-to-lyrics-generation) | 11 | 直接相关的研究线索 | 本轮仅元数据；2023 年后未见 push，许可证 API 为 NOASSERTION，未当可直接复用实现。 |
| [Suno Field Guide](https://github.com/mttkllr/suno-field-guide/tree/6813f193d72cb47088e687e0c1ea9b61c1097f3c) | 27 | 社区技巧索引与反例 | 读 README；旧型号建议与现行官方 v6 文档冲突，且有未证实的内部机理和巨大统计数字，不能照搬。 |

另外检查了华为预训练模型父仓库（3,168 星），未定位到尝试路径下可读取的 SongRewriter 实现；父仓库热度不能当该方法的落地证据。腾讯原始 tencent-ailab/SongGeneration 本轮 API 返回 404，保留可用性缺口，不以旧星数或社区 fork 冒充原仓库当前状态。

## 从具体实现中学到什么

### 1. SongMASS：先把曲拆成可对齐的单位

[推理脚本](https://github.com/microsoft/muzic/blob/2b8739671ba06f819f31f568b8a79da581aaf6f9/songmass/infer_lyric.sh)明确将 melody 设为输入、lyric 设为输出，并生成多个候选。[数据脚本](https://github.com/microsoft/muzic/blob/2b8739671ba06f819f31f568b8a79da581aaf6f9/songmass/data/generate_lmd_dataset.py)编码音高、时值、休止以及词和句的边界。这支持本项目先做完整乐句表，再比较同一乐句的改写。它不证明输出会自动保留指定笑点或英语自然重音。

### 2. SongComposer：旋律必须是输入的一部分

[inference.ipynb](https://github.com/pjlab-songcomposer/songcomposer/blob/86c1deec706aaa9195dde8bf4fbc107c6a6b21c2/inference.ipynb)包含明确的 melody-to-lyric 示例，按行提供结构化旋律，另有歌曲续写任务。可借鉴其逐行输入和全曲上下文；不复制成“让 LLM 看到歌名就能按曲写词”。

### 3. REFFLY：先明确要说什么，再逐句改到可唱

[论文](https://arxiv.org/abs/2409.00292)／[方法正文](https://arxiv.org/html/2409.00292v2)研究将内容草稿改写成给定旋律可唱的歌词：提取音乐约束，结合上下文生成候选，再对齐重要词与突出音符。对本项目最有用的是保留每句的语义和笑点功能，同时反复修句。论文结果属于作者实验；本轮未找到并验证其可直接部署的官方 GitHub 实现，不填星数、不声称复现。

### 4. 专业作词：音节总数相同仍可能唱不顺

[Berklee 的语言重音教学](https://college.berklee.edu/news/2273/berklee-riffs-natural-music-in-language)强调自然语言重音；[Pat Pattison 的 Writing Lyrics to Music 介绍](https://www.patpattison.com/online-courses)列出强弱拍、押韵位置、旋律段落和语气；[prosody 公开课文](https://online.berklee.edu/takenote/prosody-in-music-and-songwriting/)要求各部分服务同一表达。这里采用这些公开原则，不复制书籍正文。

不要机械采用“重音必须在第 1、3 拍”或“高音必是重读”的简化说法。真实曲子可能有切分、弱起、跨拍延音；以具体乐句为准。英文单词数量不是音节数；一音多音节与一音节跨多个音符也要分别处理。

## 本项目可执行流程

1. **锁定完整版本。** 区分原曲 MV、英语华尔街改词版和 Suno 既有短参考。记录版本、总长、段落与重复关系；取全曲所有完整乐句，不能把 8 秒参考延长当作整首旋律已锁定。
2. **建立乐句约束表。** 每行记录段落／乐句 ID、实际起止、弱起、音节槽位、强重音位置、停顿、尾音／拖音、押韵位及重复组。不能仅用原中文的字数猜全部节奏。未听辨或没有谱的项标 unknown。
3. **先安排内容功能。** 给每句分配一个动作：交代事件、铺垫、包袱、升级、回扣。事实与证据独立；猜测以角色／评论区口吻出现。副歌表达撑场子的核心态度，主歌负责具体场面。
4. **建立韵脚与短语候选。** 按实际发音选押韵；主包袱优先落在收束／强调处。科技专名和缩写单列发音及音节风险，避免一行堆满 NVIDIA、GPU、CUDA、export control 等长串信息。
5. **同句生成少量不同改写。** 每句保留内容意图和目标重音，改动词序、同义词、缩写或句式来适配旋律。先淘汰事实错、丢笑点或明显塞不进去的候选，不为凑韵破坏自然英语。
6. **对原旋律通唱全曲。** 检查不是只读起来押韵。重复旋律对应句的密度与落字应兼容；保留正常换气和包袱后的反应空隙。参考视频只研究机制，不搬运其完整词句。
7. **分开交付三份文本。** 阅读／字幕版保留正常拼写；逐句工作表保留音节、重音、事实标签与修改原因；Suno 输入版只含要唱的词和少量结构提示，Style 单独放。
8. **全曲范围下逐段验音频。** 先完整词稿，再选择最难乐句验证词曲适配；全曲每个乐句都要回到原旋律核对。旋律、唱词、梗、咬字分别验收，不能用音质漂亮掩盖改曲或漏词。

这套流程是本项目的整合方案，并非某个仓库已有的同名完整功能。整句候选数、质量表、梗安排均是项目制作选择，不伪装成论文标准。

## 社区检索带来的实用补充

[SunoAI 的分段制作案例](https://www.reddit.com/r/SunoAI/comments/1jncgm4/step_by_step_guide_radioready_suno_hits/)给出了生成片段链接，作者以分段增补与修补完善歌曲；可以借鉴“先定位哪一两句不行”。其大量抽取次数、播放量和音质结论均是作者自述，不继承为本项目预算或保证。[自然歌词流程帖](https://www.reddit.com/r/SunoAI/comments/1of8wt9/my_complete_workflow_for_writing_authentic_lyrics/)强调口语、具体细节、第二段推进和出声检查；其统一音节范围只作经验，不能覆盖既定旋律的具体约束。

## 当前验收边界

- 已完成：既有研究复用；多路 GitHub／论文／社区检索；星数、许可元数据与部分 commit 固定；关键 README、实际推理／数据代码和专业方法阅读；形成本地流程。
- 研究阶段尚未完成：这些模型的本机推理、全曲逐音对齐、英文成词与 Suno 新音轨。后续英文 v2 与两首在线候选已产生，见 [制作记录](../projects/jensen-song-2026-11-17/SUNO-RUN-20261117.md)；全曲音乐听辨仍未通过。
- 研究对象与引用已足够支持下一步；后续优先验证全曲曲式与参考视频机制，不继续无界扩充工具清单。
