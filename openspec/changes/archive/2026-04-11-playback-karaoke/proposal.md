## Why

小孩練習英文台詞時，需要更好的播放控制（暫停/繼續）以及視覺引導（知道目前唸到哪個字），幫助跟讀和記憶。

## What Changes

- 播放按鈕改為播放/暫停切換：播放中顯示暫停符號，暫停時顯示播放符號，點擊可切換
- 利用 edge-tts 的 word boundary 事件，在產生音檔時同時擷取每個英文單字的時間戳
- 將時間戳資料嵌入 `index.html`，播放英文音檔時逐字高亮（karaoke 效果），讓小孩知道目前唸到哪裡

## Non-Goals

- 中文音檔不做逐字高亮（中文斷詞複雜，且主要練習目標是英文）
- 不改變現有的速度控制功能

## Capabilities

### New Capabilities

- `play-pause-toggle`: 播放按鈕支援播放/暫停切換
- `word-karaoke`: 英文音檔播放時逐字高亮顯示

### Modified Capabilities

- `practice-webpage`: 整合新的播放控制和 karaoke UI
- `audio-generation`: 產生音檔時同時擷取 word boundary 時間戳

## Impact

- 修改檔案：`generate_audio.py`（擷取 word boundary、嵌入時間戳、更新 HTML 模板）、`index.html`（由腳本重新產生）
