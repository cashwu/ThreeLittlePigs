#!/usr/bin/env python3
"""Generate The Ant and The Grasshopper audio and storybook webpage."""

import asyncio
import json
import re
import sys
import tempfile
from pathlib import Path

import edge_tts

STORY_MD_PATH = Path("story.md")
STORY_ZH_PATH = Path("story_zh.json")
STORY_JSON_PATH = Path("story.json")
AUDIO_DIR = Path("audio")
HTML_PATH = Path("index.html")

EN_VOICE = "en-US-JennyNeural"
PAGE_HEADING = re.compile(r"^## p\.(\d+)$")
SENTENCE_BOUNDARY = re.compile(r'([.!?]"?)\s+(?=[A-Z"])')
VOWELS = frozenset("aeiou")


def split_sentences(text: str) -> list[list[str]]:
    """Split page text into sentences while preserving display line breaks."""
    sentences: list[list[str]] = []
    for paragraph in re.split(r"\n\s*\n", text.strip()):
        if not paragraph.strip():
            continue
        marked = SENTENCE_BOUNDARY.sub(r"\1\0", paragraph)
        for sentence in marked.split("\0"):
            lines = [line.strip() for line in sentence.splitlines() if line.strip()]
            if lines:
                sentences.append(lines)
    return sentences


def add_learning_pauses(text: str) -> str:
    """Prevent consonant-to-vowel liaison in the synthesized reading."""
    words = text.split()
    for index in range(len(words) - 1):
        next_word = words[index + 1].lstrip("\"'([{")
        current_word = words[index].rstrip("\"')]}")
        previous_letter = current_word[-1:].lower()
        if (
            next_word
            and next_word[0].lower() in VOWELS
            and previous_letter.isalpha()
            and previous_letter not in VOWELS
            and not current_word.endswith((",", ".", ";", ":", "!", "?"))
        ):
            words[index] += ","
    return " ".join(words)


def parse_story(path: Path = STORY_MD_PATH) -> list[dict]:
    """Parse story.md into an ordered list of pages and sentence lines."""
    pages: list[dict] = []
    current_page: str | None = None
    current_lines: list[str] = []

    def append_page() -> None:
        if current_page is None:
            return
        pages.append(
            {
                "page": current_page,
                "sentences": [
                    {"en_lines": lines}
                    for lines in split_sentences("\n".join(current_lines))
                ],
            }
        )

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        heading = PAGE_HEADING.fullmatch(raw_line.strip())
        if heading:
            append_page()
            current_page = heading.group(1)
            current_lines = []
        elif current_page is None:
            if raw_line.strip():
                raise ValueError("story.md content must follow a ## p.<n> heading")
        else:
            current_lines.append(raw_line)

    append_page()
    return pages


def load_translations(path: Path = STORY_ZH_PATH) -> dict[str, list[str]]:
    """Load the page-keyed Chinese translations."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("story_zh.json must contain a JSON object")
    for page_number, translations in data.items():
        if not isinstance(translations, list) or not all(
            isinstance(translation, str) for translation in translations
        ):
            raise ValueError(
                f"Page p.{page_number}: Chinese translations must be a list of strings"
            )
    return data


def combine_story(pages: list[dict], translations: dict[str, list[str]]) -> list[dict]:
    """Validate page counts and combine English sentences with translations."""
    combined: list[dict] = []
    for page in pages:
        page_number = page["page"]
        english_sentences = page["sentences"]
        chinese_sentences = translations.get(page_number, [])
        english_count = len(english_sentences)
        chinese_count = len(chinese_sentences)
        if page_number not in translations or english_count != chinese_count:
            raise ValueError(
                f"Page p.{page_number}: {english_count} English sentences "
                f"but {chinese_count} Chinese translations"
            )

        combined.append(
            {
                "page": page_number,
                "sentences": [
                    {"en_lines": sentence["en_lines"], "zh": zh}
                    for sentence, zh in zip(english_sentences, chinese_sentences)
                ],
            }
        )
    return combined


def write_story_json(pages: list[dict]) -> None:
    STORY_JSON_PATH.write_text(
        json.dumps(pages, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


async def generate_audio_with_timing(text: str, output_path: Path) -> list[dict]:
    """Generate one English MP3 and capture its word-boundary timing."""
    communicate = edge_tts.Communicate(text, EN_VOICE, boundary="WordBoundary")
    timings: list[dict] = []

    with output_path.open("wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                timings.append(
                    {
                        "word": chunk["text"],
                        "offset": round(chunk["offset"] / 10_000_000, 3),
                    }
                )
    return timings


async def generate_all_audio(pages: list[dict]) -> set[str]:
    """Generate all audio in staging, then publish it after every stream succeeds."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    expected_files: set[str] = set()

    with tempfile.TemporaryDirectory(prefix=".generate-", dir=AUDIO_DIR) as temp_dir:
        staging_dir = Path(temp_dir)
        for page in pages:
            page_number = int(page["page"])
            for sentence_index, sentence in enumerate(page["sentences"], start=1):
                filename = f"en_p{page_number:02d}_{sentence_index:02d}.mp3"
                expected_files.add(filename)
                sentence["audio"] = f"audio/{filename}"
                text = add_learning_pauses(" ".join(sentence["en_lines"]))
                sentence["timings"] = await generate_audio_with_timing(
                    text, staging_dir / filename
                )
                print(f"Generated {filename}")

        for filename in sorted(expected_files):
            (staging_dir / filename).replace(AUDIO_DIR / filename)

    return expected_files


def javascript_json(value: object) -> str:
    """Serialize trusted story data without allowing a closing script tag."""
    return json.dumps(value, ensure_ascii=False, indent=2).replace("</", "<\\/")


def generate_html(pages: list[dict]) -> None:
    """Generate the standalone storybook practice webpage."""
    pages_json = javascript_json(pages)
    html = rf"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Ant and The Grasshopper - Storybook Practice</title>
<style>
* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}
html {{
  scroll-behavior: auto;
}}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #fef9ef;
  color: #333;
  padding: 20px;
  max-width: 700px;
  margin: 0 auto;
  overflow-x: hidden;
}}
h1 {{
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  color: #e67e22;
}}
.tab-bar {{
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
  overflow-x: auto;
  padding: 10px 0;
  margin-bottom: 12px;
  background: #fef9ef;
  scrollbar-width: thin;
}}
.tab-btn {{
  flex: 0 0 auto;
  padding: 8px 14px;
  border: 2px solid #e67e22;
  border-radius: 18px;
  background: #fff;
  color: #e67e22;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}}
.tab-btn.active {{
  background: #e67e22;
  color: #fff;
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
}}
.speed-btn.active {{
  background: #e67e22;
  color: #fff;
}}
.page-section {{
  display: none;
}}
.page-section.active {{
  display: block;
}}
.line-card {{
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}}
.line-num {{
  display: inline-block;
  width: 28px;
  height: 28px;
  margin-bottom: 8px;
  border-radius: 50%;
  background: #e67e22;
  color: #fff;
  text-align: center;
  line-height: 28px;
  font-size: 14px;
  font-weight: bold;
}}
.en-row, .zh-row {{
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 8px;
}}
.en-text {{
  flex: 1;
  min-width: 0;
  font-size: 28px;
  line-height: 1.5;
  overflow-wrap: anywhere;
}}
.zh-text {{
  flex: 1;
  min-width: 0;
  margin-left: 50px;
  color: #888;
  font-size: 20px;
  line-height: 1.5;
  overflow-wrap: anywhere;
}}
.play-btn {{
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 0;
  border-radius: 50%;
  background: #3498db;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
}}
.play-btn:active {{
  transform: scale(0.9);
}}
.play-btn.playing {{
  background: #e74c3c;
}}
.word-highlight {{
  color: #e74c3c;
  font-weight: bold;
}}
@media (max-width: 480px) {{
  body {{
    padding: 12px;
  }}
  .line-card {{
    padding: 14px;
  }}
  .en-text {{
    font-size: 24px;
  }}
  .zh-text {{
    font-size: 18px;
  }}
}}
</style>
</head>
<body>
<h1>The Ant and The Grasshopper</h1>

<nav class="tab-bar" aria-label="Story pages"></nav>

<div class="speed-bar" aria-label="Playback speed">
  <button class="speed-btn" data-rate="0.33">慢慢</button>
  <button class="speed-btn active" data-rate="0.5">正常</button>
</div>

<!-- Chinese playback buttons are intentionally not rendered. -->
<main id="pages"></main>

<script>
const PAGES = {pages_json};

const PLAY_ICON = "\u25B6";
const PAUSE_ICON = "\u23F8";

let currentAudio = null;
let currentBtn = null;
let currentSentenceKey = null;
let currentTimings = [];
let playbackRate = 0.5;

function sentenceKey(pageNumber, sentenceIndex) {{
  return "p" + String(pageNumber).padStart(2, "0") + "-" +
    String(sentenceIndex).padStart(2, "0");
}}

function clearHighlights(key) {{
  if (!key) return;
  document.querySelectorAll("#en-words-" + key + " .word-span").forEach((span) => {{
    span.classList.remove("word-highlight");
  }});
}}

function stopCurrent() {{
  if (!currentAudio) return;
  currentAudio.pause();
  currentAudio.currentTime = 0;
  if (currentBtn) {{
    currentBtn.classList.remove("playing");
    currentBtn.textContent = PLAY_ICON;
  }}
  clearHighlights(currentSentenceKey);
  currentAudio = null;
  currentBtn = null;
  currentSentenceKey = null;
  currentTimings = [];
}}

function updateHighlight() {{
  if (!currentAudio || !currentSentenceKey || !currentTimings.length) return;
  const spans = document.querySelectorAll(
    "#en-words-" + currentSentenceKey + " .word-span"
  );
  if (spans.length !== currentTimings.length) return;

  let activeIndex = -1;
  for (let index = 0; index < currentTimings.length; index += 1) {{
    if (currentAudio.currentTime >= currentTimings[index].offset) {{
      activeIndex = index;
    }}
  }}
  spans.forEach((span, index) => {{
    span.classList.toggle("word-highlight", index === activeIndex);
  }});
}}

function handlePlayClick(button, pageNumber, sentenceIndex, sentence) {{
  if (currentBtn === button && currentAudio) {{
    if (currentAudio.paused) {{
      currentAudio.play();
      button.classList.add("playing");
      button.textContent = PAUSE_ICON;
    }} else {{
      currentAudio.pause();
      button.classList.remove("playing");
      button.textContent = PLAY_ICON;
    }}
    return;
  }}

  stopCurrent();
  const audio = new Audio(sentence.audio);
  const key = sentenceKey(pageNumber, sentenceIndex);
  audio.playbackRate = playbackRate;
  currentAudio = audio;
  currentBtn = button;
  currentSentenceKey = key;
  currentTimings = sentence.timings || [];

  clearHighlights(key);
  button.classList.add("playing");
  button.textContent = PAUSE_ICON;
  audio.addEventListener("timeupdate", updateHighlight);
  audio.addEventListener("ended", () => {{
    if (currentAudio !== audio) return;
    button.classList.remove("playing");
    button.textContent = PLAY_ICON;
    clearHighlights(key);
    currentAudio = null;
    currentBtn = null;
    currentSentenceKey = null;
    currentTimings = [];
  }});
  audio.play();
}}

function appendPlainLines(container, lines) {{
  lines.forEach((line, lineIndex) => {{
    if (lineIndex > 0) container.appendChild(document.createElement("br"));
    container.appendChild(document.createTextNode(line));
  }});
}}

function appendKaraokeLines(container, lines, timings) {{
  const lineTokens = lines.map((line) => line.split(/\s+/));
  const tokenCount = lineTokens.reduce((total, tokens) => total + tokens.length, 0);
  if (tokenCount !== timings.length) {{
    appendPlainLines(container, lines);
    return;
  }}

  let tokenIndex = 0;
  lineTokens.forEach((tokens, lineIndex) => {{
    if (lineIndex > 0) container.appendChild(document.createElement("br"));
    tokens.forEach((token, indexInLine) => {{
      if (indexInLine > 0) container.appendChild(document.createTextNode(" "));
      const span = document.createElement("span");
      span.className = "word-span";
      span.dataset.wordIndex = String(tokenIndex);
      span.textContent = token;
      container.appendChild(span);
      tokenIndex += 1;
    }});
  }});
}}

function renderPages() {{
  const tabBar = document.querySelector(".tab-bar");
  const pagesContainer = document.getElementById("pages");

  PAGES.forEach((page, pageIndex) => {{
    const tab = document.createElement("button");
    tab.className = "tab-btn" + (pageIndex === 0 ? " active" : "");
    tab.type = "button";
    tab.dataset.page = page.page;
    tab.textContent = "p." + page.page;
    tab.setAttribute("aria-selected", pageIndex === 0 ? "true" : "false");
    tabBar.appendChild(tab);

    const section = document.createElement("section");
    section.className = "page-section" + (pageIndex === 0 ? " active" : "");
    section.dataset.page = page.page;

    page.sentences.forEach((sentence, sentenceOffset) => {{
      const sentenceIndex = sentenceOffset + 1;
      const key = sentenceKey(page.page, sentenceIndex);
      const card = document.createElement("article");
      card.className = "line-card";

      const number = document.createElement("span");
      number.className = "line-num";
      number.textContent = String(sentenceIndex);
      card.appendChild(number);

      const englishRow = document.createElement("div");
      englishRow.className = "en-row";
      const playButton = document.createElement("button");
      playButton.className = "play-btn en";
      playButton.type = "button";
      playButton.textContent = PLAY_ICON;
      playButton.setAttribute(
        "aria-label",
        "Play page " + page.page + ", sentence " + sentenceIndex
      );
      playButton.addEventListener("click", () => {{
        handlePlayClick(playButton, page.page, sentenceIndex, sentence);
      }});
      englishRow.appendChild(playButton);

      const englishText = document.createElement("div");
      englishText.className = "en-text";
      englishText.id = "en-words-" + key;
      appendKaraokeLines(englishText, sentence.en_lines, sentence.timings || []);
      englishRow.appendChild(englishText);
      card.appendChild(englishRow);

      const chineseRow = document.createElement("div");
      chineseRow.className = "zh-row";
      const chineseText = document.createElement("div");
      chineseText.className = "zh-text";
      chineseText.textContent = sentence.zh;
      chineseRow.appendChild(chineseText);
      card.appendChild(chineseRow);

      section.appendChild(card);
    }});

    pagesContainer.appendChild(section);
  }});

  tabBar.addEventListener("click", (event) => {{
    const selectedTab = event.target.closest(".tab-btn");
    if (!selectedTab) return;
    stopCurrent();

    document.querySelectorAll(".tab-btn").forEach((tab) => {{
      const selected = tab === selectedTab;
      tab.classList.toggle("active", selected);
      tab.setAttribute("aria-selected", selected ? "true" : "false");
    }});
    document.querySelectorAll(".page-section").forEach((section) => {{
      section.classList.toggle(
        "active",
        section.dataset.page === selectedTab.dataset.page
      );
    }});

    const selectedPage = document.querySelector(
      '.page-section[data-page="' + selectedTab.dataset.page + '"]'
    );
    const targetTop = selectedPage.offsetTop - tabBar.offsetHeight - 8;
    window.scrollTo(0, Math.max(0, targetTop));
  }});
}}

document.querySelectorAll(".speed-btn").forEach((button) => {{
  button.addEventListener("click", () => {{
    document.querySelector(".speed-btn.active").classList.remove("active");
    button.classList.add("active");
    playbackRate = Number(button.dataset.rate);
    if (currentAudio) currentAudio.playbackRate = playbackRate;
  }});
}});

renderPages();
</script>
</body>
</html>
"""
    HTML_PATH.write_text(html, encoding="utf-8")


def remove_orphaned_audio(expected_files: set[str]) -> None:
    for path in AUDIO_DIR.iterdir():
        if path.is_file() and path.name not in expected_files:
            path.unlink()


async def main() -> None:
    try:
        pages = combine_story(parse_story(), load_translations())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error

    write_story_json(pages)
    print(f"Wrote {STORY_JSON_PATH} (50 sentences)")

    print("Generating English audio files...")
    expected_files = await generate_all_audio(pages)
    generate_html(pages)
    print(f"Generated {HTML_PATH}")
    remove_orphaned_audio(expected_files)
    print(f"Generated {len(expected_files)} audio files in {AUDIO_DIR}/")


if __name__ == "__main__":
    asyncio.run(main())
