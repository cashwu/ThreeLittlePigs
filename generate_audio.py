#!/usr/bin/env python3
"""Generate audio files and index.html for English lines practice."""

import asyncio
import json
import os
import sys

import edge_tts

# --- Configuration ---

ENG_MD_PATH = "eng.md"
LINES_JSON_PATH = "lines.json"
AUDIO_DIR = "audio"
HTML_PATH = "index.html"

EN_VOICE = "en-US-JennyNeural"
ZH_VOICE = "zh-TW-HsiaoChenNeural"

# Hardcoded Chinese translations (must match eng.md line count)
CHINESE_TRANSLATIONS = [
    "嗨，親愛的朋友們！我們試過稻草和木頭，但都不夠堅固！",
    "現在我們需要又硬、又重、又超級堅固的東西！",
    "我好興奮！我們終於可以安全又溫暖地待在裡面了！",
    "不用再逃跑了，今天不會再有房子倒塌了！",
    "磚頭蓋的房子夠堅固，能擋住大野狼嗎？",
    "大家小心蓋，要蓋得穩、蓋得堅固！",
    "我們的房子是磚頭做的，超級堅固！",
    "謝謝你，磚頭，保護了我們的安全！",
    "我們在堅固的磚頭屋裡，安全又快樂！",
]


def parse_eng_md(path: str) -> list[str]:
    """Parse eng.md: every non-empty line is one entry, strip '- ' prefix."""
    lines = []
    with open(path, encoding="utf-8") as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if not stripped:
                continue
            if stripped.startswith("- "):
                stripped = stripped[2:].strip()
            lines.append(stripped)
    return lines


def build_lines_json(en_lines: list[str], zh_lines: list[str]) -> list[dict]:
    """Pair English and Chinese lines into a list of dicts."""
    return [{"en": en, "zh": zh} for en, zh in zip(en_lines, zh_lines)]


async def generate_audio(text: str, voice: str, output_path: str) -> None:
    """Generate a single MP3 file using edge-tts."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


async def generate_audio_with_timing(text: str, voice: str, output_path: str) -> list[dict]:
    """Generate MP3 and capture word boundary timing data."""
    communicate = edge_tts.Communicate(text, voice, boundary="WordBoundary")
    word_timings = []

    with open(output_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                offset_seconds = chunk["offset"] / 10_000_000  # 100-ns units to seconds
                word_timings.append({
                    "word": chunk["text"],
                    "offset": round(offset_seconds, 3),
                })

    return word_timings


async def generate_all_audio(lines: list[dict]) -> list[list[dict]]:
    """Generate all English and Chinese MP3 files. Returns word timing data for English lines."""
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Generate English audio with word timing (sequential to collect per-line timing)
    all_timings = []
    for i, line in enumerate(lines):
        idx = f"{i + 1:02d}"
        timings = await generate_audio_with_timing(
            line["en"], EN_VOICE, os.path.join(AUDIO_DIR, f"en_{idx}.mp3")
        )
        all_timings.append(timings)

    # Generate Chinese audio in parallel (no timing needed)
    zh_tasks = []
    for i, line in enumerate(lines):
        idx = f"{i + 1:02d}"
        zh_tasks.append(generate_audio(line["zh"], ZH_VOICE, os.path.join(AUDIO_DIR, f"zh_{idx}.mp3")))
    await asyncio.gather(*zh_tasks)

    return all_timings


def generate_html(lines: list[dict], word_timings: list[list[dict]]) -> None:
    """Generate index.html with line data and word timing embedded inline."""
    lines_json_str = json.dumps(lines, ensure_ascii=False, indent=2)
    timings_json_str = json.dumps(word_timings, ensure_ascii=False, indent=2)
    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Three Little Pigs - Lines Practice</title>
<style>
* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #fef9ef;
  color: #333;
  padding: 20px;
  max-width: 700px;
  margin: 0 auto;
}}
h1 {{
  text-align: center;
  font-size: 28px;
  margin-bottom: 24px;
  color: #e67e22;
}}
.line-card {{
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}
.line-num {{
  display: inline-block;
  background: #e67e22;
  color: #fff;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  text-align: center;
  line-height: 28px;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}}
.en-row, .zh-row {{
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 8px;
}}
.en-text {{
  font-size: 28px;
  line-height: 1.5;
  flex: 1;
}}
.zh-text {{
  font-size: 20px;
  line-height: 1.5;
  color: #888;
  flex: 1;
}}
.play-btn {{
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s;
}}
.play-btn:active {{
  transform: scale(0.9);
}}
.play-btn.en {{
  background: #3498db;
  color: #fff;
}}
.play-btn.zh {{
  background: #2ecc71;
  color: #fff;
}}
.play-btn.playing {{
  background: #e74c3c;
}}
.word-highlight {{
  color: #e74c3c;
  font-weight: bold;
}}
.speed-bar {{
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}}
.speed-btn {{
  padding: 10px 20px;
  border-radius: 20px;
  border: 2px solid #e67e22;
  background: #fff;
  color: #e67e22;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.15s;
}}
.speed-btn.active {{
  background: #e67e22;
  color: #fff;
}}
</style>
</head>
<body>

<h1>Three Little Pigs</h1>
<p style="text-align:center; font-size:20px; color:#888; margin-bottom:20px;">Ryan - pig 2</p>

<div class="speed-bar">
  <button class="speed-btn" data-rate="0.33">慢2倍</button>
  <button class="speed-btn" data-rate="0.5">慢1倍</button>
  <button class="speed-btn active" data-rate="0.75">正常</button>
</div>

<div id="lines"></div>

<script>
const LINES = {lines_json_str};
const TIMINGS = {timings_json_str};

let currentAudio = null;
let currentBtn = null;
let currentLineIdx = -1;
let playbackRate = 0.75;

const PLAY_ICON = '\u25B6';
const PAUSE_ICON = '\u23F8';

document.querySelectorAll('.speed-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelector('.speed-btn.active').classList.remove('active');
    btn.classList.add('active');
    playbackRate = parseFloat(btn.dataset.rate);
    if (currentAudio) {{
      currentAudio.playbackRate = playbackRate;
    }}
  }});
}});

function clearHighlights(lineIdx) {{
  if (lineIdx < 0) return;
  const spans = document.querySelectorAll(`#en-words-${{lineIdx}} .word-span`);
  spans.forEach(s => s.classList.remove('word-highlight'));
}}

function stopCurrent() {{
  if (currentAudio) {{
    currentAudio.pause();
    currentAudio.currentTime = 0;
    if (currentBtn) {{
      currentBtn.classList.remove('playing');
      currentBtn.textContent = PLAY_ICON;
    }}
    clearHighlights(currentLineIdx);
    currentAudio = null;
    currentBtn = null;
    currentLineIdx = -1;
  }}
}}

function updateHighlight() {{
  if (!currentAudio || currentLineIdx < 0) return;
  const timings = TIMINGS[currentLineIdx];
  if (!timings || !timings.length) return;
  const spans = document.querySelectorAll(`#en-words-${{currentLineIdx}} .word-span`);
  if (spans.length !== timings.length) return;
  const t = currentAudio.currentTime;
  let activeIdx = -1;
  for (let i = 0; i < timings.length; i++) {{
    if (t >= timings[i].offset) activeIdx = i;
  }}
  spans.forEach((s, i) => {{
    if (i === activeIdx) s.classList.add('word-highlight');
    else s.classList.remove('word-highlight');
  }});
}}

function handleClick(btn, lineIdx, isEnglish) {{
  // Same button: toggle play/pause
  if (currentBtn === btn && currentAudio) {{
    if (currentAudio.paused) {{
      currentAudio.play();
      btn.classList.add('playing');
      btn.textContent = PAUSE_ICON;
    }} else {{
      currentAudio.pause();
      btn.classList.remove('playing');
      btn.textContent = PLAY_ICON;
      // Highlight persists on pause — do not clear
    }}
    return;
  }}

  // Different button: stop previous, start new
  stopCurrent();
  const idx = String(lineIdx + 1).padStart(2, '0');
  const src = isEnglish ? `audio/en_${{idx}}.mp3` : `audio/zh_${{idx}}.mp3`;
  const audio = new Audio(src);
  audio.playbackRate = playbackRate;
  currentAudio = audio;
  currentBtn = btn;
  currentLineIdx = isEnglish ? lineIdx : -1;

  btn.classList.add('playing');
  btn.textContent = PAUSE_ICON;

  if (isEnglish) {{
    clearHighlights(lineIdx);
    audio.addEventListener('timeupdate', updateHighlight);
  }}

  audio.addEventListener('ended', () => {{
    btn.classList.remove('playing');
    btn.textContent = PLAY_ICON;
    clearHighlights(currentLineIdx);
    currentAudio = null;
    currentBtn = null;
    currentLineIdx = -1;
  }});

  audio.play();
}}

const container = document.getElementById('lines');
LINES.forEach((line, i) => {{
  const idx = String(i + 1).padStart(2, '0');
  const card = document.createElement('div');
  card.className = 'line-card';

  // Build English text with word spans for karaoke
  const words = line.en.split(/\\s+/);
  const timings = TIMINGS[i] || [];
  let enHtml;
  if (words.length === timings.length) {{
    enHtml = words.map(w => `<span class="word-span">${{w}}</span>`).join(' ');
  }} else {{
    enHtml = line.en;
  }}

  card.innerHTML = `
    <span class="line-num">${{i + 1}}</span>
    <div class="en-row">
      <button class="play-btn en" data-line="${{i}}" data-lang="en">${{PLAY_ICON}}</button>
      <div class="en-text" id="en-words-${{i}}">${{enHtml}}</div>
    </div>
    <div class="zh-row">
      <button class="play-btn zh" data-line="${{i}}" data-lang="zh">${{PLAY_ICON}}</button>
      <div class="zh-text">${{line.zh}}</div>
    </div>
  `;
  container.appendChild(card);
}});

document.querySelectorAll('.play-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const lineIdx = parseInt(btn.dataset.line);
    const isEnglish = btn.dataset.lang === 'en';
    handleClick(btn, lineIdx, isEnglish);
  }});
}});
</script>

</body>
</html>"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)


async def main():
    # 1. Parse eng.md
    en_lines = parse_eng_md(ENG_MD_PATH)

    # 2. Fail-fast count check
    if len(en_lines) != len(CHINESE_TRANSLATIONS):
        print(
            f"Mismatch: {len(en_lines)} English lines but "
            f"{len(CHINESE_TRANSLATIONS)} Chinese translations",
            file=sys.stderr,
        )
        sys.exit(1)

    # 3. Build and write lines.json
    lines = build_lines_json(en_lines, CHINESE_TRANSLATIONS)
    with open(LINES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lines, f, ensure_ascii=False, indent=2)
    print(f"Wrote {LINES_JSON_PATH} ({len(lines)} entries)")

    # 4. Generate audio files
    print("Generating audio files...")
    word_timings = await generate_all_audio(lines)
    print(f"Generated {len(lines) * 2} audio files in {AUDIO_DIR}/")

    # 5. Generate index.html
    generate_html(lines, word_timings)
    print(f"Generated {HTML_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
