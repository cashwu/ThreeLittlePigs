## 1. 音檔產生 — 擷取 word boundary 時間戳

- [x] 1.1 修改 `generate_audio.py` 的英文音檔產生邏輯，改用 `edge_tts.Communicate.stream()` 擷取 `WordBoundary` 事件，收集每個英文單字的 text 和 offset（秒）（capture word boundary timing、generate English audio files with word timing）
- [x] 1.2 將收集到的 word timing 資料嵌入 `index.html` 作為 JS 變數（single source of truth for lines and translations — 同時嵌入 lines 和 timing 資料）

## 2. 播放控制 — 播放/暫停切換

- [x] 2.1 修改 HTML 模板的播放按鈕邏輯（play/pause toggle button）：播放中顯示 ⏸、暫停時顯示 ▶，點擊切換播放/暫停狀態，支援從暫停位置繼續播放
- [x] 2.2 更新 single active playback 規則：切換到不同句時，前一句的按鈕重置為 ▶，且清除暫停狀態（play English audio per line、play Chinese audio per line）

## 3. Karaoke 高亮

- [x] 3.1 修改 HTML 模板，用 whitespace split 將英文文字拆成逐字 `<span>`（canonical tokenization and alignment），若 span 數量與 timing 數量不符則 fallback 為不拆分的單一文字區塊（token count mismatch falls back gracefully）
- [x] 3.2 實作 `timeupdate` 事件監聽，用 `audio.currentTime` 比對 offset 高亮對應的英文單字（word-by-word karaoke highlighting），速度改變時仍正確追蹤（karaoke works with speed control）
- [x] 3.3 播放結束、切換句子時清除所有高亮（highlight resets on stop、highlight resets on new playback）；暫停時保留當前高亮（highlight persists on pause）

## 4. 驗證

- [x] 4.1 重新執行 `python generate_audio.py`，驗證 word timing 資料正確嵌入、index.html 正常顯示
- [x] 4.2 在瀏覽器中測試播放/暫停切換、karaoke 高亮、速度切換交互
