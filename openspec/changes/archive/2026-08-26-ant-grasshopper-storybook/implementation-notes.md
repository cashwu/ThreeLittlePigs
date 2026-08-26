<!-- cash-apply implementation notes | change: ant-grasshopper-storybook | initialized: 2026-08-26 19:25 | no entries below means no deviations or open questions were recorded -->

## 2026-08-26 19:25 — 缺少可逐頁核對的繪本來源
- 類別：open-question
- 任務：1.1
- 內容：repository 與目前可取得的公開資料皆未包含 12 頁完整繪本文字及版面，無法依 task 要求原樣謄打並逐頁目視比對；需要使用者提供頁面圖片／PDF，或明確決定把 contract 改為自編版本。
- 原因：以推測文字或其他版本代替會改變使用者可見故事內容、換行與驗收基準，屬於 contract／範圍變更，不能在 cash-apply 中自行決定。

## 2026-08-26 19:25 — 已改為不依賴實體繪本頁面
- 類別：deviation
- 任務：1.1
- 內容：使用者確認不需要繪本頁面後，已透過 cash-ingest 將 artifacts 同步為由本變更編寫完整、連貫且適合兒童跟讀的英文故事，仍維持 12 頁、50 句、既定關鍵例句與所有資料／UI contract。
- 原因：此決定解除原 open-question；內容來源 contract 已正式更新，因此 apply 可在不假裝逐頁謄打的前提下繼續。

## 2026-08-26 20:35 — TTS 先寫 staging 再發布正式音檔
- 類別：deviation
- 任務：5.1
- 內容：原設計以正式檔路徑直接接收循序 TTS 串流；review 發現中途失敗會先截斷既有 MP3，因此改為先把 50 句全部寫入 `audio/` 內的 staging 目錄，全部成功後才以 `Path.replace()` 發布正式音檔。
- 原因：替代手段不改變檔名、資料形狀、輸出順序、失敗模式或驗收標準，且不需要設計外的同步 primitive、identity/generation type 或 state machine；它使既有「網路中斷時正式音檔與舊 `index.html` 維持可用」contract 真正成立。
