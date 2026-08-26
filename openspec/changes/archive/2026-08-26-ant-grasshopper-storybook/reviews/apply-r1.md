# Cash Apply Review — Round 1

## Reviewer Findings

### Critical

無。

### Warning

- severity: Warning
  confidence: 99
  layer: design
  location: `generate_audio.py:119-127`
  introduced_by: `generate_audio.py:119` 直接以 `output_path.open("wb")` 開啟正式 MP3 路徑
  summary: edge-tts 串流中途失敗時會先截斷正式 MP3，使舊 `index.html` 引用不完整音檔，違反「目前可用的網頁維持可用」失敗保證。
  recommendation: 先將全部音檔寫入 staging，全部成功後才發布正式音檔。
  reviewer source: Reviewer A — Adherence、Reviewer B — Quality

### Suggestion

- severity: Suggestion
  confidence: 93
  layer: design
  location: `generate_audio.py:50-55,67-82`
  summary: `load_translations()` 未驗證每頁值為 `list[str]`，長度剛好相同的字串可能被逐字當成翻譯而靜默產生錯誤內容。
  recommendation: 在任何輸出前驗證每頁翻譯均為 `list[str]`，錯誤時回報頁碼並停止。
  reviewer source: Reviewer B — Quality

## Rating

- Critical: 0
- Warning: 1
- Non-blocking triaged findings: 1
- critical_gap: false
- round_type: full

本輪為 unseeded first full round；唯一存續的 Warning 進入 cumulative blocking set，因此必須修正並進入下一輪驗證，decision 為 `next_round`。

## Fix Actions

- 已修正 Warning：更新 `generate_audio.py`，使用 `TemporaryDirectory` 將 50 個 MP3 全部寫入 `audio/` 內 staging，全部成功後才以 `Path.replace()` 發布；更新 `design.md`、`tasks.md` 與 `implementation-notes.md`，同步說明機制替換與失敗保證。
- 已修正 Suggestion：更新 `generate_audio.py`，在輸出前驗證 `story_zh.json` 每頁值皆為 `list[str]`，型別錯誤時回報頁碼。
- 回歸驗證：模擬第二次 edge-tts 串流失敗，確認正式 MP3 byte-for-byte 不變、staging 被清除；測試含 mutation assertion，若串流改回正式音檔路徑會失敗。另驗證無效翻譯型別被拒絕。
- 完整驗證：重新執行 `uv run --with edge-tts python generate_audio.py`，成功產生 50 個 MP3、`story.json` 與 `index.html`；`python3 -m py_compile generate_audio.py` 與 Cash validation 通過。
- 修正傳播與 post-fix mechanical self-check：`staging`、`非原子`、`部分更新` 與 `Path.replace()` 已跨 `generate_audio.py`、`design.md`、`tasks.md`、`implementation-notes.md` grep 核對；spec annotation/separator、50 音檔集合與 `state: all_done` 均通過。

## Decision

next_round
