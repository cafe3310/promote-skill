#!/usr/bin/env python3
"""Cross-platform audio helper: tells the user they said 'promote' but meant 'prompt'."""
import os
import subprocess
import platform
import sys

# Path to the pre-generated voice clip (relative to repository root)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MP3_PATH = os.path.join(_SCRIPT_DIR, "..", "voice.mp3")

ZH_TEXT = (
    "我注意你刚才说了 promote，"
    "你可能是想说 prompt。"
    "模型提示词这个单词的发音是 prompt，"
    "不是 promote。"
    "都 2026 年了，别再读错了！"
)

EN_TEXT = (
    "I noticed you just said promote. "
    "You probably meant prompt. "
    "The word for AI model instructions is pronounced prompt, "
    "not promote."
)


def play_mp3(path: str) -> bool:
    """Try to play an MP3 file using a platform-appropriate player.

    Returns True on success, False if no suitable player was found.
    """
    os_type = platform.system()
    if os_type == "Darwin":
        result = subprocess.run(["afplay", path], capture_output=True)
        if result.returncode != 0:
            print(
                f"[promote-skill] afplay failed: {result.stderr.decode(errors='replace')}",
                file=sys.stderr,
            )
            return False
        return True
    if os_type == "Linux":
        for player in ["mpg123", "mpg321", "ffplay", "mplayer"]:
            result = subprocess.run(
                [player, path], capture_output=True
            )
            if result.returncode == 0:
                return True
        return False
    if os_type == "Windows":
        abs_path = os.path.abspath(path).replace("\\", "\\\\")
        # Use SoundPlayer for WAV; for MP3 fall back to Windows Media Player CLI
        ps_cmd = (
            "Add-Type -AssemblyName PresentationCore; "
            f"$p = New-Object System.Windows.Media.MediaPlayer; "
            f"$uri = [System.IO.Path]::GetFullPath('{abs_path}'); "
            "$p.Open([uri]$uri); $p.Play(); "
            "do { Start-Sleep -m 200 } while ($p.NaturalDuration.HasTimeSpan -and "
            "$p.Position -lt $p.NaturalDuration.TimeSpan); $p.Stop()"
        )
        return subprocess.run(
            ["powershell", "-Command", ps_cmd], capture_output=True
        ).returncode == 0
    return False


def speak_macos() -> None:
    """Use macOS `say`. Try Chinese voice first, fall back to English."""
    result = subprocess.run(
        ["say", "-v", "Ting-Ting", ZH_TEXT], capture_output=True
    )
    if result.returncode != 0:
        print("[promote-skill] Chinese voice unavailable, falling back to English.", file=sys.stderr)
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
            # Both TTS engines failed; print ASCII-safe English text as last-resort fallback
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
    # Prefer the pre-generated voice clip when available
    if os.path.isfile(MP3_PATH) and play_mp3(MP3_PATH):
        return

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
