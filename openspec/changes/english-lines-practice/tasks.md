## 1. 資料準備

- [x] 1.1 建立 `generate_audio.py`，解析 `eng.md`（parse eng.md into lines.json）：每個非空行為一句台詞、去掉 `- ` 前綴（不做合併），搭配硬編碼中文翻譯寫入 `lines.json`（single source of truth for lines and translations）
- [x] 1.2 加入數量驗證（fail-fast on count mismatch）：英文行數與中文翻譯數量不符時印出錯誤訊息並中止，不產生任何檔案

## 2. 音檔產生

- [x] 2.1 [P] 使用 edge-tts 產生英文音檔（generate English audio files），從 `lines.json` 讀取，產生 `audio/en_01.mp3` 到 `audio/en_09.mp3`，若 `audio/` 不存在則自動建立（audio directory creation）
- [x] 2.2 [P] 使用 edge-tts zh-TW 語音產生中文音檔（generate Chinese audio files），從 `lines.json` 讀取，儲存為 `audio/zh_01.mp3` 到 `audio/zh_09.mp3`
- [x] 2.3 執行 `generate_audio.py` 並驗證 `audio/` 下有 18 個 mp3 檔案，英文與中文順序一致

## 3. 練習網頁

- [x] 3.1 在 `generate_audio.py` 中加入產生 `index.html` 的邏輯（display all lines with translations），將台詞資料內嵌為 JS 變數，頁面可直接用 `file://` 開啟，以 child-friendly layout 呈現，英文大字、中文小字
- [x] 3.2 為每句英文和中文各加上播放按鈕（play English audio per line、play Chinese audio per line），實作 single active playback 規則：任何新播放都停止目前播放，不分英文中文
- [x] 3.3 確保網頁在手機和平板上可正常瀏覽（responsive layout）

## 4. UI 增強

- [x] 4.1 在 `generate_audio.py` 的 HTML 模板中，將英文字體從 22px 加大到 28px、中文字體從 16px 加大到 20px（child-friendly layout 更新）
- [x] 4.2 在 HTML 模板頂部加入播放速度控制按鈕（playback speed control）：「慢2倍」(0.5x)、「慢1倍」(0.75x)、「正常」(1.0x)，預設為「正常」，當前速度高亮顯示
- [x] 4.3 速度設定須即時套用到正在播放的音檔，並持續影響後續所有播放
- [x] 4.4 重新執行 `python generate_audio.py` 產生更新後的 `index.html`，驗證速度切換功能正常
