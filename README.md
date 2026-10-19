# 视频创作 / Video Creation

维护准备发布的视频 ideas 与不同栏目。入口是简洁的栏目/想法卡片；AI 音乐只是其中一个栏目，研究、操作方案和真实实验放在独立详情页。不做后台或复杂创作平台。

公开页面：<https://farmcan.pages.dev/creation/>。由网站杂货铺首页进入；使用现有 farmcan Pages 项目，不额外占用 Cloudflare 项目。页面免登录、免密码。

## 栏目与当前状态

- [栏目与 ideas](https://farmcan.pages.dev/creation/)：AI 音乐、职场小剧场、AI 工具日常；候选栏目和待策划想法明确标记。
- [AI 音乐详情](https://farmcan.pages.dev/creation/ai-music/)：参考、制作方案、实验进展与验收。主路线是 Suno：8 秒原曲片段已实际入库，换词生成待验；28 秒版本的拒绝保留为历史记录。本地开源路线已停止，没有本地生成音轨。
- `projects/catalog.json` 维护栏目与 idea；`projects/ai-music.json` 维护音乐实验状态。技术细节不再占满总入口。

## 维护与发布

需要 Python 3，无第三方构建依赖。

```sh
python3 scripts/build.py
python3 scripts/export.py --target ../farmcan-websites
```

只在 main 维护。先提交并推送本仓库，再导出；本仓库的源版本和首页、AI 音乐详情与静态资源哈希写入 build-manifest.json。导出后在既有 farmcan-websites 仓库构建、检查、commit/push，复用 Actions 发布与 release.json / 首页哈希验收，并额外核验 creation 页的字节。

- `projects/`：结构化状态、路线、验收标准、选题与参考链接。
- `research/`：原创研究与操作笔记。
- `site/`：静态界面模板与原创图标。
- `dist/`：不提交的生成页面，只显式导出选定文件。

## 公开边界

普通研究、视频 ideas、计划、操作和真实进展默认公开。第三方完整歌词、原媒体、截图、个人财务、账号凭证、身份信息不进入公开仓库或网页。技术权限已开与生成成功分别记录，环境通过不冒充模型推理完成，播放量是注明日期的样本快照，不保证流量。

研究继承自同一维护者先前的原创 AI 音乐制作笔记，保留原平台与工具官方链接，不继承第三方词曲、录音或截图。源码、界面和原创文档使用 MIT；外部作品与工具权利仍归各自权利人。
