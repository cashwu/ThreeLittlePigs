# Verification

驗證輸出行為，不只驗證函式存在或字串出現。

## Source and data

- 頁 ID 的順序、數量與輸入一致。
- 每頁至少一個非空句子；每個 `en_lines` fragment 已 trim 且非空。
- 所有來源圖片或文字頁都被消費一次，沒有漏頁或重複頁。
- 每頁英文與中文句數相同，總句數相同。
- 段落強制分句、引句加 reporting clause、行中句界各至少以一個真實或構造案例驗證。
- 中介 JSON 可解析，且只包含預期 schema。

## Failure boundaries

- 以暫時缺少一筆翻譯或錯誤 value type 的輸入執行，確認在任何正式 audio、HTML 或中介輸出變更前失敗，錯誤包含頁碼。
- 模擬 TTS 在第二個或中間句子失敗，確認正式音檔 byte-for-byte 不變、staging 無殘留、既有 HTML 未覆寫。
- 對上述測試加入有限 mutation check，例如讓 mock 拒絕直接指向正式 `audio/` 的 output path，確保測試真的能抓到回歸。

## Audio and karaoke

- 音檔數恰等於句數，命名與頁內序號一致，且每個檔案非空。
- `audio/` 不包含上一版孤兒檔、中文音檔或暫存目錄。
- 每句顯示 token 數等於 timing 數；列出所有 mismatch，而不是只報總數。
- 每句 offset 單調不遞減。
- 至少播放一個跨顯示換行的句子，確認高亮越過 `<br>` 後仍依序前進。
- 若啟用幼兒學習停頓，驗證顯示文字不變、TTS token 數不變，並抽查至少一個目標邊界（例如 `was always`）確實產生較清楚的停頓。

## Browser acceptance

以 `file://` 開啟輸出並驗證：

- 標題正確，沒有上一個故事殘留的 title、heading 或副標。
- tab 數、順序、預設頁與頁數一致；恰有一個 active tab。
- 每頁可見卡片數等於資料；隱藏頁仍保留在 DOM。
- 切頁回到該頁頂端，切回後按鈕與事件仍可用。
- 播放／暫停可切換；暫停保留高亮；切頁與播放另一句都停止舊音訊。
- 速度設定立即生效並跨頁保持。
- 手機 viewport 下 tab 不折行、可橫向捲動，document 不水平溢出。
- standalone 頁面不依賴 runtime fetch；音檔只在使用者播放時載入。

## Docker acceptance

若有 Docker 支援：

- `docker compose config` 成功。
- image build 成功。
- 暫時啟動後首頁回傳成功，內容包含正確 title 或 heading。
- 對一個 MP3 發送 `Range: bytes=0-9`，應得到 `206 Partial Content`、正確 `Content-Range` 與 `Accept-Ranges: bytes`。
- healthcheck 進入 healthy。
- 若使用者沒有要求持續執行，驗證後執行 `docker compose down`；image 可保留。

## Generated artifact drift

任何 HTML、CSS 或 JavaScript 修正後都重新執行產生器。確認產生後的 `index.html` 保留修正；不要以直接手改 generated HTML 作為最終解法。
