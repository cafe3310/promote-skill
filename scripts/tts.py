#!/usr/bin/env python3
"""Cross-platform TTS helper: tells the user they said 'promote' but meant 'prompt'."""
import subprocess
import platform
import sys


ZH_TEXT = (
    "我注意你刚才说了 promote，"
    "你可能是想说 prompt。"
    "prompt 的发音是 prɒmpt，"
    "不是 prəˈmoʊt。"
)

EN_TEXT = (
    "I noticed you just said promote. "
    "You probably meant prompt. "
    "Prompt is pronounced as p-r-o-m-p-t, "
    "not p-r-o-m-o-t-e."
)


def speak_macos() -> None:
    """Use macOS `say`. Try Chinese voice first, fall back to English."""
    result = subprocess.run(
        ["say", "-v", "Ting-Ting", ZH_TEXT], capture_output=True
    )
    if result.returncode != 0:
        print(f"[promote-skill] Chinese voice unavailable, falling back to English.", file=sys.stderr)
        subprocess.run(["say", EN_TEXT], check=True)


def speak_linux() -> None:
    """Use espeak-ng (Chinese) or espeak (English) on Linux."""
    result = subprocess.run(
        ["espeak-ng", "-v", "zh", ZH_TEXT], capture_output=True
    )
    if result.returncode != 0:
        result2 = subprocess.run(
            ["espeak", EN_TEXT], capture_output=True
        )
        if result2.returncode != 0:
            # Both TTS engines failed; print English text as last-resort fallback
            print(EN_TEXT, file=sys.stderr)


def speak_windows() -> None:
    """Use Windows SAPI via PowerShell."""
    ps_cmd = (
        "Add-Type -AssemblyName System.Speech; "
        f"(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{EN_TEXT}')"
    )
    result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
    if result.returncode != 0:
        print(f"[promote-skill] Windows TTS failed: {result.stderr.decode(errors='replace')}", file=sys.stderr)


def main() -> None:
    os_type = platform.system()
    if os_type == "Darwin":
        speak_macos()
    elif os_type == "Linux":
        speak_linux()
    elif os_type == "Windows":
        speak_windows()
    else:
        print(ZH_TEXT)


if __name__ == "__main__":
    main()
