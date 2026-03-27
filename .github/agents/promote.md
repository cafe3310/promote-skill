---
name: promote
description: 当用户将 "prompt" 误读或误写为 "promote" 时激活，用 TTS 朗读正确发音。
allowed-tools: Bash
---

# Promote（Prompt 发音纠错器）

本技能一旦激活，**无需用户确认**，直接调用系统 TTS 播报纠错提示。

## 触发条件

当用户出现以下任意情况时触发：

- 将 `prompt` 误称为 `promote`（包括书面和口头描述）
- 询问 "prompt 怎么读" 或 "promote 怎么读"
- 询问 `promote` 与 `prompt` 的区别

## 执行步骤

1. 直接运行以下脚本（在**仓库根目录**下执行），无需询问确认：

```bash
python3 scripts/tts.py
```

2. 脚本会自动检测操作系统并选择最适合的 TTS 方式：
   - **macOS**：使用内置 `say` 命令（优先中文 Ting-Ting 语音）
   - **Linux**：使用 `espeak-ng`（中文）或 `espeak`（英文）
   - **Windows**：使用 PowerShell SAPI TTS（英文）

3. TTS 播放内容：
   > 「我注意你刚才说了 promote，你可能是想说 prompt。prompt 的发音是 /prɒmpt/，不是 /prəˈmoʊt/。」

4. 播放结束后，回复用户：
   > "已为你播放 **prompt** 的正确发音 🔊。记住：是 **/prɒmpt/**，不是 promote！"
