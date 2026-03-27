# promote-skill 🔊

> **prompt** ≠ **promote** — 帮你分清这两个词的 GitHub Copilot Agent Skill

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-演示页面-blue?logo=github)](https://cafe3310.github.io/promote-skill/)

## 一句话安装

将以下这句话发给你的 **GitHub Copilot Agent**，即可完成安装：

```
请从 https://github.com/cafe3310/promote-skill 安装 promote skill，将 .github/agents/promote.md 复制到我的仓库中。
```

或者手动把 [`.github/agents/promote.md`](.github/agents/promote.md) 复制到你自己仓库的 `.github/agents/` 目录下。

---

## 功能说明

当你（或你的 AI 助手）把 `prompt` 说成 / 写成 `promote` 时，Skill 会自动激活：

1. **检测操作系统**
2. **调用系统 TTS**，朗读纠错提示：
   > 「我注意你刚才说了 promote，你可能是想说 prompt。
   > prompt 的发音是 /prɒmpt/，不是 /prəˈmoʊt/。」
3. **回复用户**正确拼写和发音

| 平台 | TTS 方式 |
|------|----------|
| macOS | `say -v Ting-Ting` |
| Linux | `espeak-ng -v zh` / `espeak`（fallback） |
| Windows | PowerShell SAPI |

---

## 文件结构

```
.github/agents/promote.md   ← Copilot Agent Skill 定义
scripts/tts.py              ← 跨平台 TTS 脚本
index.html                  ← GitHub Pages 演示页面
```

---

## 发音速查

| 词 | 音标 | 备注 |
|----|------|------|
| **prompt** | /prɒmpt/ | ✅ 你想说的 |
| **promote** | /prəˈmoʊt/ | ❌ 你以为你在说的 |
