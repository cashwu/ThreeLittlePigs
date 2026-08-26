# page-navigation Specification

## Purpose

page-navigation capability.

## Requirements

### Requirement: 頁碼 tab 列

網頁 SHALL 在畫面最上方顯示一列水平的頁碼 tab，位置在播放速度控制之上、所有句子卡片之上。繪本的每一頁 SHALL 對應一個 tab，標籤採用繪本自身的頁碼、格式為 `p.<n>`。tab SHALL 依繪本頁序排列。任何時刻 SHALL 恰有一個 tab 處於選中狀態，且選中的 tab SHALL 在視覺上與未選中的 tab 有所區別。

tab 列 SHALL 以 sticky 方式固定於視窗頂端，在頁面捲動時維持可見，並 SHALL 具有不透明背景，使捲動中的句子卡片 SHALL NOT 自其下方透出而與 tab 標籤重疊。

tab 列 SHALL NOT 換行；在寬度不足以容納全部 tab 時，SHALL 由 tab 列自身橫向捲動，使其恆為一行高、不因 sticky 而長期占用 viewport 高度。此處的橫向捲動 SHALL 僅限 tab 列自身這個導覽元素；句子卡片的英文與中文內文 SHALL NOT 需要橫向捲動即可閱讀，body 亦 SHALL NOT 出現水平捲軸。

在手機寬度的 viewport 下，tab 列 SHALL 維持可操作，且 body SHALL NOT 出現水平捲軸。

#### Scenario: 依繪本頁序渲染所有 tab

- **WHEN** 使用者在瀏覽器中開啟 `index.html`，包含以 `file://` 開啟
- **THEN** 畫面最上方 SHALL 顯示 12 個 tab，依序標示為 `p.2`、`p.3`、`p.4`、`p.5`、`p.6`、`p.7`、`p.8`、`p.10`、`p.12`、`p.14`、`p.15`、`p.16`

#### Scenario: 捲動時 tab 列維持可見

- **WHEN** 使用者在句子較多的頁（例如 `p.12`，共 7 張卡片）向下捲動到該頁底部
- **THEN** tab 列 SHALL 仍然可見且標籤清晰可讀，卡片內容 SHALL NOT 自 tab 列下方透出與其重疊，使用者 SHALL NOT 需要先捲回頁面頂端才能切換頁

#### Scenario: 手機寬度下 tab 列維持一行高

- **WHEN** 在寬度不足以並排 12 個 tab 的 viewport 下檢視網頁
- **THEN** tab 列 SHALL 維持一行高並可橫向捲動至其餘的 tab，SHALL NOT 折行成多行，且 body SHALL NOT 出現水平捲軸

#### Scenario: 恰有一個 tab 被選中

- **WHEN** 網頁處於任何狀態
- **THEN** SHALL 恰有一個 tab 帶有選中樣式，其餘 11 個 SHALL 帶有未選中樣式

<!-- @trace
source: ant-grasshopper-storybook
updated: 2026-08-26
code:
tests:
-->

### Requirement: 載入時的預設頁

網頁載入時，繪本的第一頁 SHALL 被選中，且該頁的句子卡片 SHALL 是唯一可見的卡片。

#### Scenario: 載入時顯示第一頁

- **WHEN** 使用者開啟 `index.html`
- **THEN** `p.2` 這個 tab SHALL 處於選中狀態，且 SHALL 只有屬於第 2 頁的句子卡片可見

<!-- @trace
source: ant-grasshopper-storybook
updated: 2026-08-26
code:
tests:
-->

### Requirement: 只有被選中頁的句子可見

任何時刻 SHALL 至多只有一頁的句子卡片可見。選中某個 tab SHALL 使該頁的句子卡片變為可見，並隱藏其他所有頁的句子卡片，同時 SHALL 把捲動位置回到該頁頂端。被隱藏的頁 SHALL 保留在 document 中，使其播放按鈕與逐字高亮元素在切頁前後維持相同的身分與事件繫結。

#### Scenario: 切換 tab 會替換可見的頁

- **WHEN** 目前選中 `p.2`，使用者點擊 `p.12` 這個 tab
- **THEN** `p.12` SHALL 變為選中、`p.2` SHALL 變為未選中，第 12 頁的句子卡片 SHALL 變為可見，第 2 頁的句子卡片 SHALL 被隱藏

#### Scenario: 切換頁面後捲動位置回到頁首

- **WHEN** 使用者在 `p.12` 捲動到該頁底部，然後點擊 `p.16` 這個 tab（該頁只有 2 張卡片）
- **THEN** 捲動位置 SHALL 回到該頁頂端，使 `p.16` 的第一張卡片可見

#### Scenario: 回到先前瀏覽過的頁

- **WHEN** 使用者先選 `p.12`，再選回 `p.2`
- **THEN** 第 2 頁的句子卡片 SHALL 再度可見，且行為 SHALL 與剛載入網頁時完全相同，包含播放按鈕顯示為播放符號

##### Example: 各頁的句子卡片數

| Tab | 顯示的句子卡片數（等於該頁在 `story.json` 中的句子數） |
| ---- | -------------------- |
| p.2  | 4 |
| p.3  | 4 |
| p.4  | 3 |
| p.5  | 5 |
| p.6  | 3 |
| p.7  | 5 |
| p.8  | 5 |
| p.10 | 4 |
| p.12 | 7 |
| p.14 | 5 |
| p.15 | 3 |
| p.16 | 2 |

<!-- @trace
source: ant-grasshopper-storybook
updated: 2026-08-26
code:
tests:
-->

### Requirement: 切換頁面會停止播放

選中頁碼 tab SHALL 停止任何正在播放或處於暫停狀態的音訊。被停止的句子，其播放按鈕 SHALL 重設為播放符號（▶），其逐字高亮 SHALL 被清除，以免看不見的頁仍在播音或停留在暫停狀態。

#### Scenario: 使用者切頁時播放中的音訊停止

- **WHEN** 第 2 頁的某個句子正在播放，使用者點擊 `p.4` 這個 tab
- **THEN** 音訊 SHALL 停止，該句子的按鈕 SHALL 重設為播放符號（▶），其逐字高亮 SHALL 被清除，且 SHALL 沒有任何音訊在播放

#### Scenario: 使用者切頁時暫停中的音訊被清除

- **WHEN** 第 2 頁的某個句子播到一半被暫停，使用者點擊 `p.4` 這個 tab，之後再點回 `p.2`
- **THEN** 該句子的按鈕 SHALL 顯示播放符號（▶）且沒有任何字被高亮，點擊後 SHALL 從頭開始播放

#### Scenario: 點擊已經被選中的 tab

- **WHEN** 第 2 頁的某個句子正在播放，使用者點擊已經選中的 `p.2` 這個 tab
- **THEN** 音訊 SHALL 停止，按鈕 SHALL 重設為播放符號（▶），且第 2 頁 SHALL 維持為可見的頁

<!-- @trace
source: ant-grasshopper-storybook
updated: 2026-08-26
code:
tests:
-->
