## MODIFIED Requirements

### Requirement: Capture word boundary timing

在產生英文音訊的過程中，腳本 SHALL 為每個英文句子擷取 edge-tts 的 word boundary 事件。每個 word boundary 事件 SHALL 包含該字的文字與其起始時間 offset（以秒為單位）。由於一個句子是把其顯示行以空白串接後合成為一個音檔，這些 offset SHALL 相對於該句子音檔的起點。時間資料 SHALL 直接掛在該句子的物件上（欄位名為 `timings`），與 `en_lines`、`zh`、`audio` 並列，隨頁與句子的資料一併以單一 JavaScript 變數 `PAGES` 的形式內嵌於 `index.html`。SHALL NOT 存在以全域句子索引定位的獨立時間資料陣列，以免「頁加頁內序號」與「跨頁流水號」兩套索引空間並存時，因流水計數器錯位而讓某句對到別句的時間軸。

#### Scenario: 逐字時間資料的結構

- **WHEN** 產生 `index.html`
- **THEN** 每個英文句子的 `timings` SHALL 是一個物件陣列，各物件含 `word`（字串）與 `offset`（數值，單位為秒）欄位，掛在 `PAGES` 中該句子的物件上

#### Scenario: 不存在獨立的全域時間資料陣列

- **WHEN** 檢視產生出的 `index.html` 所內嵌的 JavaScript 變數
- **THEN** 逐字時間資料 SHALL 只能透過 `PAGES` 中該句子的物件取得，SHALL NOT 有另一個以全域句子索引定位的時間資料陣列

#### Scenario: 時間 offset 單調不遞減

- **WHEN** 檢視某個英文句子的時間資料
- **THEN** 每一筆的 `offset` SHALL 大於或等於前一筆的 `offset`

### Requirement: Canonical tokenization and alignment

網頁 SHALL 把每個英文句子的文字渲染為個別的 `<span>` 元素。tokenization 規則 SHALL 為：把該句子的顯示行以單一空白串接，再以空白切分其結果（等同於 `en_lines.join(' ').split(/\s+/)`）。每個切出的 token 成為一個 `<span>`。由於 `en_lines` 的每個元素皆為已去除首尾空白的非空字串，此切分 SHALL NOT 產生空字串 token；若顯示行帶有前導空白，`split(/\s+/)` 會於陣列開頭多出一個空字串而使 token 數與 `timings` 長度差 1，導致該句靜默失去高亮。

一個句子的 `<span>` 元素 SHALL 以整句為範圍連續編號，跨越標記繪本換行的 `<br>` 元素。`<br>` SHALL NOT 重新開始編號，使索引為 N 的 span 恆對應同一句子的第 N 筆 word boundary 資料。

`<span>` 元素的數量 SHALL 等於該句子 `timings` 中 word boundary 的筆數。兩者數量不符時，網頁 SHALL 退回把該句子顯示為保留 `<br>` 換行的文字，不做 `<span>` 切分、該句子不做逐字高亮。SHALL NOT 拋出錯誤；播放 SHALL 仍正常運作、只是沒有高亮，其他句子 SHALL NOT 受影響。

#### Scenario: tokenization 與時間資料相符

- **WHEN** 某個英文句子在其所有顯示行上共有 12 個以空白分隔的 token，且有 12 筆 word boundary 資料
- **THEN** 網頁 SHALL 渲染 12 個 `<span>` 元素，並依索引把每個 span 對應到其時間資料

#### Scenario: span 編號跨越換行延續

- **WHEN** 某個句子的顯示行為 `["Once upon a time,", "a little ant lived in a beautiful meadow."]`
- **THEN** 第一個顯示行 SHALL 容納索引 0 至 3 的 span，其後 SHALL 接一個 `<br>`，第二個顯示行 SHALL 容納索引 4 至 11 的 span

#### Scenario: token 數不符時優雅退回

- **WHEN** 某個英文句子有 10 個以空白分隔的 token，但其時間資料只有 9 筆 word boundary
- **THEN** 網頁 SHALL 在保留該句換行的前提下不做 `<span>` 切分，該句子 SHALL NOT 有逐字高亮，且其他每一個句子 SHALL 維持其高亮

### Requirement: Word-by-word karaoke highlighting

在英文音訊播放期間，網頁 SHALL 高亮目前正被唸出的字。時間 offset 已被越過、但下一個字的 offset 尚未被越過的那個字 SHALL 以明顯的顏色被高亮。整個網頁在同一時刻 SHALL 至多只有一個字被高亮。SHALL 只有英文文字有逐字高亮；中文文字 SHALL NOT 有。

高亮 SHALL 由 Audio 元素的 `timeupdate` 事件驅動，使用 `audio.currentTime` 判定要高亮哪一個字。由於 `currentTime` 反映實際播放位置，此作法本質上 SHALL 在任何播放速度下都能追蹤到正確位置。

#### Scenario: 播放期間逐字依序高亮

- **WHEN** 某個英文音訊正在播放，且 `audio.currentTime` 越過某個字的 offset
- **THEN** 該字的 `<span>` SHALL 被高亮，且前一個字的高亮 SHALL 被移除

#### Scenario: 重新播放時高亮重設

- **WHEN** 使用者開始播放某個句子，或重播同一個句子
- **THEN** 該句子所有的逐字高亮 SHALL 在播放開始前被重設

#### Scenario: 停止時高亮清除

- **WHEN** 音訊停止，無論是因為點擊了另一個句子、切換了繪本頁，或播放到結束
- **THEN** 所有逐字高亮 SHALL 被清除

#### Scenario: 暫停時高亮保留

- **WHEN** 音訊處於暫停狀態
- **THEN** 目前被高亮的字 SHALL 維持高亮，直到播放恢復或音訊被停止

#### Scenario: 逐字高亮搭配速度控制

- **WHEN** 使用者變更播放速度
- **THEN** 逐字高亮 SHALL 仍追蹤到正確的字，因為它使用反映實際播放位置的 `audio.currentTime`
