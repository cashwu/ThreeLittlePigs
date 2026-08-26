## Summary

把英文台詞練習網頁的內容從《Three Little Pigs》的 9 句舞台台詞，換成《The Ant and The Grasshopper - Fables of Aesop》整本繪本（12 頁、50 句），並在畫面最上方加入頁面切換 tab，一次只顯示一頁。播放/暫停、逐字 karaoke 高亮、速度切換等既有行為維持不變。

## Motivation

現有內容是單一場景的片段台詞，換成整本繪本後內容橫跨 12 頁（p.2、3、4、5、6、7、8、10、12、14、15、16）。

50 句全部攤平在同一個捲動頁面上，小朋友會找不到現在唸到哪一頁。因此除了換內容之外，需要頁面切換 tab 把畫面收斂到一次一頁。

同時，上一個 commit 已經把中文播放按鈕註解掉，但 generate_audio.py 仍在產生中文音檔，規格與實作已有落差，這次一併收斂。

## Proposed Solution

- 資料來源改為 story.md（以頁碼標題分頁、編寫完整且連貫的英文故事）與 story_zh.json（頁碼對應中文句子陣列），取代 eng.md 與腳本內寫死的中文清單；分句結果落成可檢視的中介檔 story.json，取代扁平的 lines.json。
- 切句規則從「每個非空白行 = 一句」改為「照句號分句」：一個完整句子 = 一段音檔 = 一個播放按鈕；story.md 中的顯示換行只影響畫面排版，不影響音檔切割與 karaoke 對齊。
- 音檔命名從全域流水號改為頁面內流水號，讓單頁內容修改時不牽動其他頁的檔名。
- 網頁最上方新增 12 個頁碼 tab，點擊只顯示該頁的句子卡片，並停止目前播放中的音訊；預設停在 p.2。
- 中文翻譯維持「顯示但不發音」：畫面仍顯示灰色中文，中文播放按鈕維持註解狀態，且不再產生中文音檔。
- 網頁標題改為新繪本：`<title>` 與 `<h1>` 改為 The Ant and The Grasshopper，舊的 `Ryan - pig 2` 副標刪除。
- 把 commit `4114ad5` 只手改在 `index.html`、未回寫 `generate_audio.py` 模板的四項現值寫回模板（速度按鈕選項與標籤、預設播放速度、中文播放按鈕的註解狀態、中文文字縮排），否則重新產生 `index.html` 會讓這些調整倒退。

## Non-Goals

- 不做整頁連續播放（自動接續播下一句）。
- 不做上一頁／下一頁的左右箭頭或滑動手勢，只用最上方的 tab 切換。
- 不做書本插圖顯示；本次只處理文字與音訊。
- 不做中文語音；中文播放按鈕維持註解狀態。
- 不改變播放速度按鈕呈現給使用者的選項與標籤，維持目前的「慢慢」0.33 與「正常」0.5。注意這不代表「不需要動程式」—— `generate_audio.py` 的模板仍是舊的三顆按鈕與預設 0.75，需回寫成上述現值才能維持不變。
- 不保留舊的《Three Little Pigs》內容作為可切換的第二本書。

## Alternatives Considered

- **照每個顯示行切句**：語氣會在句中斷掉，例如 All summer long, the grass grew tall, 會單獨成為一段音檔，且一頁會有 7-11 個播放按鈕。
- **照空行分段切句**：一段音檔太長，小朋友不易跟讀。
- **沿用全域流水號音檔命名**：較簡單，但修改中間某一頁造成句數變動時，後面所有頁的檔名都會位移，整批音檔要重產。
- **中文寫在 story.md 裡**：會讓英文來源混入中文，也讓自動分句規則要處理中英混排。
- **用 NLP 斷句套件（如 nltk 的 punkt）**：引入額外相依，對繪本這種乾淨、無縮寫的文本沒有額外好處。

## Capabilities

### New Capabilities

- `page-navigation`: 頁面切換 tab 的呈現與行為 — 12 個頁碼 tab 的顯示、單頁可見性切換、切頁時停止播放、預設起始頁。

### Modified Capabilities

- `audio-generation`: 資料來源改為 story.md 與 story_zh.json 的頁面結構；解析規則從逐行改為照句號分句並保留換行資訊；音檔命名改為頁面內流水號；不再產生中文音檔。
- `practice-webpage`: 句子卡片改為依頁分組、一次只顯示一頁；英文句需依 `story.md` 定義的顯示換行排版；移除中文播放按鈕的需求；速度控制的規格收斂為目前實作的「慢慢」0.33 與「正常」0.5。
- `word-karaoke`: tokenization 改以「整句跨多個顯示行」為單位，詞的 span 索引需跨越換行標記連續編號，才能與 edge-tts 的整句 word boundary 對齊。

## Impact

- Affected specs: 新增 `page-navigation`；修改 `audio-generation`、`practice-webpage`、`word-karaoke`
- Affected code:
  - New:
    - `story.md` — 以頁碼標題分頁、由本變更編寫的完整英文故事
    - `story_zh.json` — 頁碼對應中文句子陣列
    - `story.json` — 分句後的中介檔
  - Modified:
    - `generate_audio.py` — 解析、分句、音檔產生、HTML 產生全部改寫
    - `index.html` — 由腳本重新產生，含 tab bar、依頁分組、多行句子排版
    - `audio/` — 整個目錄重產：新增 50 個英文句子音檔，刪除舊繪本的 18 個音檔
  - Removed:
    - `eng.md` — 由 story.md 取代
    - `lines.json` — 由 story.json 取代
- 依賴：edge-tts 套件。目前環境未安裝，改以 uv 在執行時載入該套件。
