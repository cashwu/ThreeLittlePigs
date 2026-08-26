---
name: kids-storybook-builder
description: Build or update a child-friendly bilingual storybook practice site from page-by-page English text or page images, including transcription, Chinese translations, English TTS, word-level karaoke, page navigation, optional Docker Compose, and end-to-end verification. Use for storybook reading or shadowing sites; not for illustration-only requests.
---

# Kids Storybook Builder

把逐頁英文內容製作成適合兒童跟讀的雙語故事網頁。輸入可能是使用者直接提供的逐頁英文，也可能是一組逐頁圖片。

## 核心原則

- 忠實保留使用者提供的故事內容、頁序、段落與有意義的顯示換行。除非使用者明確要求改寫，不自行補寫、潤飾或替換原文。
- 圖片中無法可靠辨識、且會影響故事內容或頁序的文字，必須指出具體頁面與片段並詢問；不要默默猜測。
- 畫面文字與語音合成文字分開處理。為幼兒加入停頓時，不得把教學用標點寫回顯示原文。
- 頁數、句數、每頁句數與檔名集合都由實際來源推導，不把某一本書的數字寫死成通用規則。
- 先驗證所有頁面的英文與中文句數，再產生任何昂貴或會覆寫正式產物的輸出。
- 產生器是 `index.html` 的唯一來源；任何 UI 修正都必須回寫模板並重新產生，避免下次執行倒退。
- 保持方案簡單：單一來源資料、頁內穩定 ID、靜態檔案與小型產生器通常已足夠。

## 輸入模式

先判斷輸入類型，只讀取對應章節：

- 使用者提供逐頁英文文字：讀 [references/input-modes.md](references/input-modes.md) 的「文字模式」。
- 使用者提供逐頁圖片：讀 [references/input-modes.md](references/input-modes.md) 的「圖片模式」。
- 兩者都有：以使用者指定的 authoritative source 為準；未指定時，以圖片核對文字並列出差異，不自行選邊。

不要因為缺少非必要資訊而停下。可從檔名、圖片頁碼、現有資料結構或專案慣例可靠推導的內容直接處理；只有會改變故事文字、頁序、語言、輸出形式或驗收結果的歧義才詢問使用者。

## 目標產物

優先沿用專案既有命名。新專案沒有慣例時使用：

- `story.md`：依 `## p.<page>` 分頁的英文來源，保留段落與顯示換行。
- `story_zh.json`：頁碼到中文句子陣列的映射。
- `story.json`：產生器輸出的中介資料，每句至少含 `en_lines` 與 `zh`。
- `audio/en_p<page>_<sentence>.mp3`：英文逐句音檔，頁碼與頁內序號補零。
- `index.html`：可由 `file://` 開啟的 standalone 練習網頁。
- `generate_audio.py` 或現有等價產生器：解析、驗證、TTS、timing、HTML 與孤兒檔清理。
- 視需求加入 `Dockerfile`、`docker-compose.yml`、`.dockerignore` 與獨立 Nginx 設定。

若專案已有不同 schema，不為了符合上述名稱而建立平行資料模型；將相同 invariants 套到現有結構。

## 實作流程

### 1. 盤點與建立來源

先檢查現有產生器、HTML、音檔命名、翻譯來源、Docker 設定與未提交變更。保留不相關工作。

依輸入建立逐頁英文來源。圖片模式必須先完成頁序與文字核對；文字模式必須保留使用者的頁界。若使用者只提供故事內容、沒有頁碼，可依明確的輸入順序建立穩定頁 ID，並在交付摘要說明。

### 2. 分句與翻譯

顯示換行不等於句界：

- 空行代表段落邊界，強制結束目前句子。
- 段落內依句尾標點與下一個大寫字母或引號判斷新句。
- 問句或引句後接小寫 reporting clause 時維持同一句，例如 `"Why?" asked the child.`。
- 句界落在顯示行中間時，將該行拆給前後兩句，並去除每個 fragment 首尾空白。

中文以英文分句為單位一對一翻譯。翻譯需自然、適齡並保留語意，不因中文標點重新改變英文句界。逐頁驗證英文與中文句數；缺頁、型別錯誤或數量不符時，在任何音檔、HTML 或中介檔覆寫前 fail fast，錯誤訊息包含頁碼與兩邊數量或實際型別。

### 3. 產生英文音檔與逐字 timing

每個句子把 `en_lines` 以單一空白串接，產生一個 MP3 並收集 word-boundary offset。正式音檔不得直接接收可能失敗的網路串流：

1. 在 `audio/` 同檔案系統建立 staging 目錄。
2. 全部句子成功產生後，再以原子 replace 發布正式檔案。
3. 寫出引用新集合的 HTML 後，才清除不屬於本次集合的孤兒音檔。
4. 中途失敗時清除 staging，保留正式音檔與目前可用的 HTML。

若目標是初學或約 4–7 歲兒童，對語音合成文字加入適度的 consonant-to-vowel 學習停頓，例如把合成用的 `was always` 變成 `was, always`：

- 只改 TTS 輸入，不改畫面英文。
- 前字已有停頓標點時不重複加入。
- 不把所有字逐字切開；只處理會明顯連讀的邊界，保持句子仍像自然朗讀。
- 加入標點前後 token 數必須相同；重新產生後逐句確認 timing 數仍與顯示 token 數一致。

若使用外部 TTS，遵守目前環境的網路與資料傳送授權要求。不要把 secrets、未授權資料或無關檔案送到外部服務。

### 4. 建立練習網頁

網頁應能直接以 `file://` 使用，不做 runtime fetch。至少提供：

- 故事標題。
- 依來源順序排列的頁碼 tab，預設第一頁，一次只顯示一頁。
- 每句的頁內序號、英文播放／暫停按鈕、保留換行的英文、中文翻譯。
- 同一時間只播放一個音檔；播放另一句或切頁時停止前一句。
- 暫停時保留目前高亮，停止或切頁時清除。
- 逐字 karaoke；同一句的 span index 跨 `<br>` 連續。
- timing/token 不符時只讓該句退回保留 `<br>` 的純文字，播放仍可用。
- 適合手機的單行可橫向捲動 tab，body 不產生水平捲軸。
- 適齡的預設速度與慢速選項；若專案已有明確設定則沿用。

資料與 timing 只使用一套定位方式。建議以 `PAGES` 內嵌頁面、句子、音檔與 timing，DOM ID 使用頁碼加頁內句號；不要再建立跨頁全域 timing index。

### 5. Docker Compose

使用者要求容器支援，或專案已採 Docker 部署時，提供小型 Nginx image：只 COPY runtime 需要的 HTML 與音檔，healthcheck 使用 base image 已具備的工具，音檔支援 byte range，HTML 不做 immutable cache。Compose 的 host port 應可由環境變數覆寫。

驗證時可暫時啟動容器；完成後預設停止，除非使用者要求保留執行中。不要在未經要求時刪除 image 或 volume。

### 6. 驗證與交付

完成後讀 [references/verification.md](references/verification.md) 並執行與風險相稱的檢查。至少驗證來源、資料形狀、完整產生、音檔集合、karaoke alignment、桌面／手機互動，以及 Docker config（若存在）。

若可使用瀏覽器自動化，實際開啟 `file://.../index.html`；有 Docker 時再驗證 HTTP 首頁與至少一個 MP3 range request。不要只靠 grep 宣告 UI 或音訊功能成功。

交付摘要需列出：頁數、句數、音檔數、輸入模式、任何無法確認的轉錄、karaoke mismatch 清單、瀏覽器驗收結果，以及 Docker 是否仍在執行。
