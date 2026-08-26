## ADDED Requirements

### Requirement: 網頁標題反映目前的繪本

網頁的 `<title>` 與 `<h1>` SHALL 標示目前的繪本名稱 `The Ant and The Grasshopper`。頁面 SHALL NOT 出現舊繪本的名稱 `Three Little Pigs`，也 SHALL NOT 出現舊的角色副標 `Ryan - pig 2`。

由於 `index.html` 完全由 `generate_audio.py` 的 HTML 模板產生，這些字串 SHALL 在模板中更新，而非只手改產出的 `index.html`。

#### Scenario: 標題顯示新的繪本名稱

- **WHEN** 使用者開啟 `index.html`
- **THEN** 瀏覽器分頁標題與頁面最上方的 `<h1>` SHALL 標示 `The Ant and The Grasshopper`，且頁面上 SHALL NOT 出現 `Three Little Pigs` 或 `Ryan - pig 2`

### Requirement: 產出的網頁與模板一致

`index.html` 是產出物而非來源檔。`generate_audio.py` 的 HTML 模板 SHALL 產生出與目前 `index.html` 相同的既有使用者可見行為，涵蓋 commit `4114ad5` 先前只手改在 `index.html` 而未回寫模板的四個項目：速度按鈕的選項與標籤、預設 `playbackRate`、中文播放按鈕的註解狀態、以及中文文字的縮排對齊。

#### Scenario: 重新產生後既有 UI 調整不倒退

- **WHEN** 執行 `generate_audio.py` 重新產生 `index.html`
- **THEN** 產出的網頁 SHALL 顯示兩顆速度按鈕「慢慢」與「正常」、預設 `playbackRate` SHALL 為 0.5、中文播放按鈕 SHALL 維持 HTML 註解狀態、中文文字 SHALL 保留其與英文文字對齊的左側縮排

##### Example: 模板需回寫的四個項目

| 項目 | 模板原值 | 應回寫為 |
| ---- | -------- | -------- |
| 速度按鈕 | `慢2倍` 0.33 / `慢1倍` 0.5 / `正常` 0.75 | `慢慢` 0.33 / `正常` 0.5 |
| 預設 `playbackRate` | 0.75 | 0.5 |
| 中文播放按鈕 | 未註解 | 以 HTML 註解輸出 |
| `.zh-text` 縮排 | 無 `margin-left` | `margin-left: 50px` |

## MODIFIED Requirements

### Requirement: Display all lines with translations

網頁 `index.html` SHALL 由 `generate_audio.py` 產生，並把所有頁與句子的資料（英文與中文）以 JavaScript 變數的形式內嵌其中。網頁 SHALL NOT 於執行時抓取外部資料檔，使其能以 `file://` 直接開啟。

句子卡片 SHALL 依繪本頁分組，同一頁的卡片 SHALL 依句子在繪本中出現的順序排列。每張句子卡片 SHALL 顯示該句在該頁內的序位數字、英文句子，以及其下方的中文翻譯。英文文字 SHALL 以顯眼的大字級呈現，中文文字 SHALL 以較小或較淡的樣式呈現於每個英文句子之下。

英文句子 SHALL 依 `story.md` 中 `en_lines` 所定義的顯示換行排版，以 `<br>` 元素呈現。

#### Scenario: 載入後依頁分組顯示整本繪本

- **WHEN** 使用者在瀏覽器中開啟 `index.html`，包含以 `file://` 開啟
- **THEN** 所有句子卡片 SHALL 依繪本頁分組存在於 document 中，每張卡片下方顯示其中文翻譯，且不需要網頁伺服器

#### Scenario: 畫面上保留繪本換行

- **WHEN** 某個句子的顯示行為 `["Once upon a time,", "a little ant lived in a beautiful meadow."]`
- **THEN** 該卡片 SHALL 把這兩行渲染為畫面上分開的兩行，中間以 `<br>` 分隔

### Requirement: Play English audio per line

每個英文句子 SHALL 有一個播放/暫停切換按鈕，用以播放或暫停該句子對應的英文 MP3 音檔。播放期間，英文文字 SHALL 顯示逐字 karaoke 高亮。

#### Scenario: 使用者點擊英文播放按鈕

- **WHEN** 使用者點擊某個英文句子旁的播放按鈕
- **THEN** 瀏覽器 SHALL 播放該句子的 `audio/en_p<page>_<index>.mp3` 檔，按鈕 SHALL 顯示暫停符號，且逐字高亮 SHALL 開始

##### Example: 播放按鈕對應的音檔

- **GIVEN** 使用者正在檢視 `p.12` 這個 tab
- **WHEN** 使用者點擊第 7 張句子卡片的播放按鈕
- **THEN** 瀏覽器 SHALL 播放 `audio/en_p12_07.mp3`

### Requirement: Single active playback

任何新的音訊播放 SHALL 停止目前正在播放或暫停中的音訊。任何時刻 SHALL 至多只有一個音檔處於作用中（播放或暫停）狀態。當某個句子的音訊被另一個句子或被切換頁面所停止時，其按鈕 SHALL 重設為播放符號（▶），且任何逐字高亮 SHALL 被清除。

#### Scenario: 播放某句後點擊另一句

- **WHEN** 某個句子的音訊正在播放，使用者點擊另一個句子的播放按鈕
- **THEN** 第一個音訊 SHALL 停止、其按鈕 SHALL 重設為播放符號（▶）、其高亮 SHALL 被清除，且第二個音訊 SHALL 以全新的高亮開始播放

#### Scenario: 暫停中的句子被新的播放所停止

- **WHEN** 某個句子的音訊處於暫停狀態，使用者點擊另一個句子的播放按鈕
- **THEN** 暫停中的音訊 SHALL 停止、其按鈕 SHALL 重設為播放符號（▶）、其高亮 SHALL 被清除，且新點擊的句子 SHALL 開始播放

### Requirement: Playback speed control

網頁 SHALL 在畫面上方顯示速度控制按鈕，位置在頁碼 tab 列之下、所有句子卡片之上。按鈕 SHALL 為「慢慢」與「正常」。目前作用中的速度 SHALL 在視覺上被標示出來。

- 「慢慢」SHALL 把 `Audio.playbackRate` 設為 0.33
- 「正常」SHALL 把 `Audio.playbackRate` 設為 0.5

預設速度 SHALL 為「正常」（0.5 倍速）。所選速度 SHALL 立即套用至目前正在播放的音訊，並套用至後續所有音訊播放，包含切換到不同繪本頁之後所播放的音訊。

#### Scenario: 使用者選擇慢速後播放音訊

- **WHEN** 使用者點擊「慢慢」，之後點擊任一播放按鈕
- **THEN** 音訊 SHALL 以 0.33 倍速播放

#### Scenario: 使用者於播放期間變更速度

- **WHEN** 音訊正在播放，使用者點擊另一個速度按鈕
- **THEN** 目前播放中的音訊 SHALL 立即改為新的速度

#### Scenario: 速度設定跨頁保持

- **WHEN** 使用者選擇「慢慢」，播放第 2 頁的某個句子，之後切換到第 4 頁並播放該頁的某個句子
- **THEN** 第 4 頁的句子 SHALL 同樣以 0.33 倍速播放

## REMOVED Requirements

### Requirement: Play Chinese audio per line

**Reason**: 中文播放按鈕先前已被註解移出網頁，且中文 MP3 檔不再產生。中文文字僅作為閱讀輔助留在畫面上。

**Migration**: 不渲染任何中文播放按鈕，且不存在任何中文 MP3 檔。中文翻譯仍顯示於每個英文句子之下。

#### Scenario: 不顯示中文播放按鈕

- **WHEN** 使用者檢視任何一張句子卡片
- **THEN** SHALL NOT 有任何中文播放按鈕可見或可點擊，且中文翻譯 SHALL 仍以文字形式顯示於英文句子之下
