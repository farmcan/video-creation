# 视频创作维护约定

- 只在 main 维护。普通创作 ideas、研究、操作方案和实际进展默认公开、免登录、免密码。
- 私人财务、账号凭证、个人身份与原媒体不进入仓库；第三方完整歌词、录音和截图不发布。
- 用已验证事实区分已完成、失败、待测与推断。没有可听音轨，不称音乐生成或复现成功。
- `projects/` 保存项目状态；`research/` 保存原创研究；Python 构建静态网页，显式导出到既有导航站的 `site/creation/`，不新建 Cloudflare 项目。
- 发布前运行 build 与隐私/链接检查。推送本仓库后，导出选定静态文件到 farmcan-websites 并推 main；核对其 Actions、release.json、首页与本页哈希。
- 不将生成失败与热点/填词质量混为一谈。先固定 30 秒词曲验证技术，再写原创填词和选题。
- 后续 Agent 先读 `docs/README.md` 和 `docs/creative-song-workflow.md`。换人物或主题时复用研究、乐句约束、铺梗／回扣和分项验收方法，重新核实事实与曲目版本，不直接套用本次新闻或歌词。
- 录音按 `docs/audio-recording.md`，本次文件索引在 `projects/jensen-song-2026-11-17/LOCAL-ASSETS.md`。音频留仓库外；当前环境不向模型工具结果注入 `input_audio`，避免重现历史会话的连续 400 错误。
