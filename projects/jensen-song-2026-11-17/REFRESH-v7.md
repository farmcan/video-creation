# v7 清晰度、起音与候选交接

当前剪映工程 `Let-Him-Cook-community-v4` 的 `v7` 时间线由 v6 复制。60 个切段、48 条字幕、1280×720 的画面轨时间线及原音乐进入位置保持；原生 1080p MOV 和交付 720p MP4 均为 30 fps、6828 帧、视频 227.600 秒。厨房封面经用户确认，作为单独封面保存。平台状态见[投稿回执](PUBLISH-v7.md)。

- 14.3 秒首次出现的观众反应及其余七处：沿用已修复 1675×939 图，撤掉为旧硬字幕设置的裁切，等比铺满 16:9。统一的字幕仍走剪映轨道。
- 31.84 秒起的舞台：从干净的红裙、黑夹克近景做 GPT 定向去糊，锁定原景别、舞姿、手的位置及粉蓝灯光，只补皮衣、头发与眼镜可读的纹理；保留原图及干净相邻帧。输出属重制，不充作真实影像。
- 77.92 秒起的机器人：换同张照片的 1200×675 版本；保持展开双臂和机器人的构图。官方新闻图的 2048×1365 广角是备选，不是假定为同帧。
- 82.16 秒的出炉：不用有绿问号的预告缩略图，换真实邻帧，脸、隔热手套、板卡和烤箱可见。后二处用 2560×1440 案板版本。真实原帧的右侧炉灶多，使用近景裁切时检查不能盖住板卡。
- 使用 GPT 图像工具生成厨房封面：以两张真实厨房照片为参考，保留烤箱、黄仁勋外观和板卡轮廓；重构为端板卡上菜的二创封面，左侧只写 `LET HIM COOK`，不加说明。原 `CHINESE MODEL?` 封面仍有本地母版。

本地版本见[图片索引](visual-assets-v7.json)：旧版、选用和备选路径相对仓库；实际第几镜及时间见其引用的 `shots-v7.json`。独立 Agent 检查原生 MOV 的 0.7、3、15.3、34.3、80、84.3、177.3、224 秒，确认满屏观众、板卡无遮挡、字幕英上中下，舞台右侧手略贴边。导出分辨率不等于源图具备同等真实细节。

## 片头试听

未在谱图发现持续的 50／60 Hz 及成串谐波，不能确认电流声具体成因；不上全曲陷波。参考[现场广播混音师案例](https://www.shure.com/en-GB/insights/reimagining-crowd-mics-for-broadcast-with-the-dca901)：主轨和观众反应分开，反应只在所需瞬间出现。实际剪辑用了 [IENBA 轻惊讶 CC0](https://freesound.org/people/IENBA/sounds/488472/)，从原公开预览 3.29–4.45 秒取样，成片 0.045 秒放入、约 1.2 秒前收完，音效峰值约 −26.5 dBFS；音乐起音前 150 ms 温和提拉。另有 [noah0189 综艺式 Oooh CC0](https://freesound.org/people/noah0189/sounds/264499/) B 试听，较明显，未入片。`local/jensen-community-v7/audio/preview-{original,A,B}.mp3` 是 10 秒对照。处理后的 PCM 自 2 秒起与旧轨逐字节一致；原生导出解码后的起音与 A 版波形对齐。未实听断言杂音已消除或歌曲同步已人工验收。

## 只供选择的后续素材

- 新增梗图：`local/jensen-community-v7/meme-options/community-3-up.jpg`，三张从左到右：[皮衣随显卡销量变亮](https://www.reddit.com/r/pcmasterrace/comments/1hvwcf4/the_more_gpus_you_buy_the_shinier_my_jacket_gets/) 可接 1:10；[问显卡定价就集体嘘](https://www.reddit.com/r/pcmasterrace/comments/1txvvsk/when_someone_asks_how_the_gpus_are_priced/) 可接 2:16；[Denny's 空卡座](https://www.reddit.com/r/SanJose/comments/1xvey2t/one_day_after_stepping_down_as_ceo_the_jensen/) 可接 2:24 回扣「留个座」。原图及使用位置均待用户审选，未改时间线。空座只表达回扣，不据此给现实事件下判断。
- 本人声音：`local/jensen-community-v7/voice-candidates/VOICE-SOURCES.md`。首选 [YC Startup School 2026](https://www.ycombinator.com/library/Tq-jensen-huang-the-mindset-that-built-nvidia) 登台说的 “Oh my God.”，官方播客 41.58–43.65 秒（2.07 秒，含现场观众底声）；次选 [Arm Tech Unheard](https://newsroom.arm.com/podcasts/tech-unheard-episode-one-jensen-huang) 62.90–65.10 秒以及 101.90–106.70 秒的两段真实采访。主办方逐字稿及本机原录音转写交叉核对，未混入成片。厨房原片另存来源线索，没取得下载的音频，不补时码。公开播放不等于再发行许可。
- [B 站、抖音和 X 投稿草稿](RELEASE-COPY-v7.md)；[换图方法](../../docs/visual-source-refresh.md)、[投稿方法](../../docs/video-release-packaging.md)。

## 语言交付分版

国内版保留英上中下的剪映成片；X 版从同一无字幕画面轨烧入英文，字幕节点沿用原有 48 条，仅去翻译。两版复用同一 AAC 音轨、画面切点和厨房封面。用户判断本轮新增梗图不够有趣，候选留档，本轮不加入；YC 原声单独给用户试听。
