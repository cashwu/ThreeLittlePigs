## MODIFIED Requirements

### Requirement: Single source of truth for lines and translations

系統 SHALL 把本變更編寫的英文故事與中文翻譯分別放在兩個權威來源檔中：

- `story.md` SHALL 存放完整、連貫且適合兒童跟讀的《The Ant and The Grasshopper》英文故事，並以 `## p.<n>` 形式的頁碼標題分組。故事 SHALL 使用第 2、3、4、5、6、7、8、10、12、14、15、16 頁與 50 句的既定結構，保留本 spec examples 指定的關鍵句。同一頁內的文字 SHALL 保留作者設定的顯示換行，以及段落之間的空行。所有引號 SHALL 使用 ASCII 直引號 `"` 與 `'`；`story.md` SHALL NOT 含有彎引號 `“`、`”`、`‘`、`’`，因為分句規則以 ASCII 引號字元判定句界。
- `story_zh.json` SHALL 存放中文翻譯，格式為一個 JSON 物件，key 為頁碼字串，value 為該頁中文句子字串的陣列，順序與該頁英文句子的順序相同。

`generate_audio.py` SHALL 由這兩個來源推導出 `story.json`，作為記錄分句結果、可供人工檢視的中介檔。`story.json` SHALL 是一個頁物件的陣列，每個頁物件有 `page` 欄位（頁碼字串）與 `sentences` 陣列，其中每個句子有 `en_lines`（顯示行的陣列）與 `zh`（中文翻譯）。

`story.json` SHALL 在逐頁句數檢查通過後、產生任何音檔之前寫出，使分句結果不必等 50 次語音合成跑完即可檢視。孤兒檔的清除 SHALL 排在 `index.html` 寫出之後，使任何中斷點上都不會出現 `index.html` 指向已被刪除音檔的狀態。

`generate_audio.py` SHALL 同時產生 `index.html`，把頁與句子的資料以及 word boundary 時間資料以 JavaScript 變數的形式內嵌其中，使網頁能以 `file://` 直接開啟、不需伺服器。

#### Scenario: story.json 的結構

- **WHEN** 任何元件讀取 `story.json`
- **THEN** 它 SHALL 是一個依繪本頁序排列的頁物件陣列，每個物件有 `"page"`（頁碼字串）與 `"sentences"`（物件陣列，各含 `"en_lines"` 陣列與 `"zh"` 字串）

##### Example: story.json 的第一頁

- **GIVEN** `story.md` 第 2 頁開頭的兩行是 `Once upon a time,` 與 `a little ant lived in a beautiful meadow.`
- **WHEN** 產生 `story.json`
- **THEN** 其第一個元素 SHALL 為 `{"page": "2", "sentences": [{"en_lines": ["Once upon a time,", "a little ant lived in a beautiful meadow."], "zh": "..."}, ...]}`

### Requirement: Fail-fast on count mismatch

對 `story.md` 中的每一頁，腳本 SHALL 驗證分句產生的英文句數等於 `story_zh.json` 中該頁列出的中文翻譯數。腳本 SHALL 同時驗證 `story_zh.json` 對 `story.md` 中出現的每一個頁碼都有對應項目。

任何一頁未通過上述任一檢查時，腳本 SHALL 以非零狀態結束，並印出指出該頁與兩邊數量的錯誤訊息。此情況下 SHALL NOT 產生任何音檔、`story.json` 或 `index.html`。

#### Scenario: 逐頁句數不符時中止產生

- **WHEN** `story.md` 第 5 頁分出 5 個英文句子，但 `story_zh.json` 為第 5 頁列出 4 個翻譯
- **THEN** 腳本 SHALL 以類似 `Page p.5: 5 English sentences but 4 Chinese translations` 的錯誤訊息結束，且不產生任何檔案

#### Scenario: 翻譯檔缺少某頁時中止產生

- **WHEN** `story.md` 含有 `## p.10` 標題，但 `story_zh.json` 沒有 `"10"` 這個 key
- **THEN** 腳本 SHALL 以非零狀態結束，在錯誤訊息中指出第 10 頁，且不產生任何檔案

### Requirement: Generate English audio files

系統 SHALL 提供一支 Python 腳本 `generate_audio.py`，使用 `edge-tts` 套件為每一個英文句子產生一個 MP3 音檔。送入語音合成引擎的文字 SHALL 是該句子的顯示行以單一空白串接後的結果，使繪本的換行不影響合成出來的語音。

產生過程中，腳本 SHALL 使用 `edge_tts.Communicate.stream()` 擷取 `WordBoundary` 事件，記錄每個字的文字與起始時間 offset（以秒為單位，由 edge-tts 提供的 100 奈秒單位換算而來）。

每個句子 SHALL 產生一個存放於 `audio/` 目錄的 MP3 檔，命名為 `en_p<page>_<index>.mp3`，其中 `<page>` 是補零至兩位的繪本頁碼，`<index>` 是該句子在該頁內的序位，從 1 起算並補零至兩位。

#### Scenario: 產生所有英文音檔並取得逐字時間

- **WHEN** 使用者執行產生腳本
- **THEN** 腳本 SHALL 為每個句子產生一個 MP3，並為每個句子蒐集 word boundary 時間資料

#### Scenario: 建立 audio 目錄

- **WHEN** `audio/` 目錄不存在
- **THEN** 腳本 SHALL 在產生檔案之前建立 `audio/` 目錄

#### Scenario: 清除不屬於本次產生結果的音檔

- **WHEN** 腳本成功產生本次的全部英文音檔
- **THEN** 腳本 SHALL 刪除 `audio/` 中所有不屬於本次產生結果的音檔，使 `audio/` 的內容恰等於本次產生的集合

##### Example: 某頁句數減少後的孤兒檔

- **GIVEN** `audio/` 中已存在上一次產生的 `audio/en_p12_07.mp3`
- **WHEN** 第 12 頁的內容被改為只有 6 句並重新執行腳本
- **THEN** 腳本 SHALL 刪除 `audio/en_p12_07.mp3`，使 `audio/` 中不留下該孤兒檔

##### Example: 音檔命名

| 頁碼 | 頁內序位 | 檔名 |
| ---- | ----------------- | --------- |
| 2 | 1 | `audio/en_p02_01.mp3` |
| 2 | 4 | `audio/en_p02_04.mp3` |
| 10 | 1 | `audio/en_p10_01.mp3` |
| 12 | 7 | `audio/en_p12_07.mp3` |
| 16 | 2 | `audio/en_p16_02.mp3` |

#### Scenario: 產生流程失敗後重跑

- **WHEN** 腳本在產生 50 個音檔的過程中，因網路中斷或服務節流而在中途失敗
- **THEN** 腳本 SHALL NOT 刪除任何既有音檔，`index.html` SHALL NOT 被覆寫，目前可用的網頁 SHALL 維持可用，且重新執行整支腳本 SHALL 重新產生全部音檔並得到與一次成功執行相同的結果

#### Scenario: 換行不切割音檔

- **WHEN** 某個句子的 `en_lines` 為 `["The ant knew that it was time", "to prepare for the coming winter."]`
- **THEN** 腳本 SHALL 把單一字串 `The ant knew that it was time to prepare for the coming winter.` 合成為一個 MP3 檔

## ADDED Requirements

### Requirement: 把 story.md 解析為頁與句子

腳本 SHALL 把 `story.md` 解析為有序的頁清單。形如 `## p.<n>` 的行 SHALL 開啟一個頁碼為 `<n>` 的新頁。兩個頁碼標題之間的所有文字 SHALL 屬於前一個頁。

在同一頁內，腳本 SHALL 依下列規則把文字切成句子。空行 SHALL 一律結束一個句子。段落之內，當句尾標點（`.`、`!` 或 `?`，其後 SHALL 允許接一個右引號）之後的下一個非空白字元是大寫字母或左引號時，SHALL 在該處放置句界。當下一個非空白字元是小寫字母時，SHALL NOT 放置句界，使引號內的對話與其後的敘述歸屬同一句。

腳本 SHALL 為每個句子記錄 `story.md` 定義的顯示換行，形式為有序的顯示行陣列。落在繪本某一行中間的句界 SHALL 把該行拆分給前後兩個句子。顯示行陣列的每一個元素 SHALL 為已去除首尾空白的非空字串，使瀏覽器端以空白切分時 SHALL NOT 產生空字串 token。

#### Scenario: 句界落在繪本行尾

- **WHEN** 某頁含有連續兩行 `for her family in the meadow.` 與 `She worked hard, and was always busy.`
- **THEN** 腳本 SHALL 產生兩個句子，因為 `.` 之後接的是大寫字母 `S`

#### Scenario: 引號對話後接小寫敘述維持同一句

- **WHEN** 某頁含有連續兩行 `"Why do you bother to work so hard?"` 與 `asked the grasshopper.`
- **THEN** 腳本 SHALL 產生一個句子，其顯示行即為這兩行繪本行，因為 `?"` 之後接的是小寫字母 `a`

#### Scenario: 行中切句後的顯示行不帶首尾空白

- **WHEN** 句界落在繪本某一行中間，例如 `he cried. "And I'm starving, too!` 被拆為兩個句子
- **THEN** 後一句的第一個顯示行 SHALL 為 `"And I'm starving, too!`，SHALL NOT 保留切點處的前導空白，使該句在瀏覽器端以空白切分後的 token 數與其 `timings` 長度相等

#### Scenario: 段落邊界結束一個句子

- **WHEN** 某頁的一個段落以 `through the long grass.` 結束，空行之後的下一段以 `"Why do you bother to work so hard?"` 開始
- **THEN** 腳本 SHALL 在段落邊界結束一個句子，不把跨越空行的兩段文字併為同一句

##### Example: 段落規則作為安全網

- **GIVEN** 某頁的一個段落以 `They ate the seeds.` 結束，空行之後的下一段以小寫字母開頭的 `and slept through the winter.` 開始
- **WHEN** 套用分句規則
- **THEN** 段落規則 SHALL 使這兩段分屬不同句子；標點規則在此不適用（`.` 之後接的是小寫字母），段落規則是唯一使其斷句的依據

#### Scenario: 句界落在繪本行中間

- **WHEN** 某頁含有繪本行 `he cried. "And I'm starving, too!`
- **THEN** 腳本 SHALL 在 `he cried.` 之後結束一個句子，並自 `"And I'm starving, too!` 開始下一個句子，把該繪本行拆分給這兩個句子

##### Example: 句界判定

| 候選句界前後的文字 | 是否切句 | 理由 |
| ---------------------------------- | ------ | ------ |
| `...in the meadow.` / `She worked hard...` | 是 | `.` 之後接大寫 `S` |
| `...so hard?"` / `asked the grasshopper.` | 否 | `?"` 之後接小寫 `a` |
| `"You are just wasting your time!"` / `he laughed.` | 否 | `!"` 之後接小寫 `h` |
| `he cried. "And I'm starving, too!` | 是 | `.` 之後接左引號 |
| `...more than enough to eat!` / `And besides, why...` | 是 | `!` 之後接大寫 `A` |
| `...only a few seeds left.` / `I'm sorry, but...` | 是 | `.` 之後接大寫 `I` |

##### Example: 各頁句數

- **GIVEN** `story.md` 含有第 2、3、4、5、6、7、8、10、12、14、15、16 這 12 頁
- **WHEN** 腳本完成解析與分句
- **THEN** 每一頁的英文句數 SHALL 等於 `story_zh.json` 中該頁的中文翻譯數；具體數值 SHALL 為 4, 4, 3, 5, 3, 5, 5, 4, 7, 5, 3, 2，合計 50 句

## REMOVED Requirements

### Requirement: Parse eng.md into lines.json

**Reason**: 新故事內容具有頁的層級，且句子跨越多個顯示行，「每個非空白行 = 一個項目」的規則無法表達這種結構。改由「把 story.md 解析為頁與句子」這條需求取代，該需求依句界切句並把繪本換行保留為顯示資訊。

**Migration**: 刪除 `eng.md` 與 `lines.json`。英文故事移至 `story.md` 的頁碼標題之下；中文翻譯從 `generate_audio.py` 內寫死的清單移至 `story_zh.json`；推導出的中介檔改為 `story.json`。

#### Scenario: eng.md 與 lines.json 已不存在

- **WHEN** 產生腳本執行
- **THEN** 它 SHALL NOT 讀取 `eng.md` 或 `lines.json`，且這兩個檔案 SHALL NOT 存在於 repository 中

### Requirement: Generate Chinese audio files

**Reason**: 中文播放按鈕並未顯示在網頁上，因此中文 MP3 檔從不會被播放。產生它們只會耗費產生時間與磁碟空間而無任何好處。

**Migration**: 刪除既有的 `audio/zh_01.mp3` 至 `audio/zh_09.mp3`，且不再產生任何中文 MP3 檔。中文翻譯仍以文字形式顯示在網頁上。

#### Scenario: 不產生任何中文音檔

- **WHEN** 產生腳本成功結束
- **THEN** `audio/` 目錄 SHALL NOT 含有任何符合 `zh_*.mp3` 的檔案
