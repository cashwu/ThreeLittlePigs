## Why

小孩要參加英文話劇表演（三隻小豬），需要背誦英文台詞。希望做一個簡單的網頁，讓小孩可以看到台詞、點擊播放英文發音來練習，同時附上中文翻譯和中文音檔方便大人講解、小孩理解。

## What Changes

- 使用 edge-tts（免費 TTS 工具）為 9 句英文台詞產生英文 mp3 音檔
- 為每句台詞的中文翻譯產生中文 mp3 音檔
- 製作一個純靜態 HTML 單頁網頁，呈現所有台詞
- 每句台詞顯示英文原文 + 中文翻譯，各有獨立的播放按鈕
- 字體大、間距寬，適合小孩閱讀
- 網頁頂部提供播放速度切換按鈕（慢2倍、慢1倍、正常），切換後影響所有音檔播放速度
- 字體再加大，提升閱讀舒適度

## Capabilities

### New Capabilities

- `audio-generation`: 使用 edge-tts 批次產生英文和中文的 mp3 音檔
- `practice-webpage`: 靜態 HTML 網頁，呈現台詞並可點擊播放音檔

### Modified Capabilities

（無）

## Impact

- 新增檔案：`generate_audio.py`（產生音檔、`lines.json`、`index.html`）、`lines.json`（台詞與翻譯的唯一資料來源）、`index.html`（由腳本產生，資料內嵌）、`audio/` 資料夾（mp3 音檔）
- 依賴：Python 套件 `edge-tts`
- 台詞來源：`eng.md`
