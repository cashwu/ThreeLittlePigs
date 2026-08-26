# Cash Propose Review — Round 3

## Reviewer Findings

本輪為 micro round，由單一 Reviewer V 對累積阻塞集合做差異驗證，並檢查第 2 輪修正的傳播與新引入的缺陷。

### 累積阻塞集合逐一判定

- **V-1**（Warning，`fix-introduced`，DOM id 全域計數器與「計數器已消失」宣稱互相矛盾）→ **resolved**。Reviewer V 查證：`design.md` 的 tab Decision 已改為頁內定位 `en-words-p<頁碼兩位>-<頁內序號兩位>`，`globalIdx` 僅以「現況、被取代的對象」身分出現一次；word boundary Decision 的結論句已改為有條件陳述；音檔名、DOM id、`timings` 三個原本需要全域索引的定位點全部改為 `(page, index)`，對照現況程式碼確認這正是舊實作中 `i` / `currentLineIdx` / `lineIdx` 三處全域索引的全部用途；`tasks.md` 4.4 的 `document.getElementById('en-words-p12-07')` 為可執行且能擋下回歸的驗證。

累積阻塞集合在本輪開始時清空。

### Warning

**R3-1**
- `severity`: Warning
- `confidence`: 85
- `layer`: design
- `location`: `design.md` →「音檔命名採頁面內流水號 `en_pNN_MM.mp3`」Decision vs `specs/audio-generation/spec.md` 清除孤兒檔 Scenario、`tasks.md` 3.1 與 5.2、`proposal.md` `## Impact`
- `summary`: 孤兒檔清除的範圍在 design 與其他所有 artifact 之間不一致。design 寫「刪除所有不屬於本次產生結果的**英文**音檔」，spec 與 tasks 3.1 皆寫「所有…音檔」。design 同一句後半「使 `audio/` 的內容恰等於本次產生的集合」也與自己前半的英文限定互相矛盾。第 2 輪 V-3 的修正把 5.2 的人工刪除移除、全權交給 3.1 之後，若實作者依 design 只清英文音檔，實際存在的 9 個 `audio/zh_*.mp3` 就沒有任何負責者，`tasks.md` 5.2 的驗證、`design.md` 的驗收條件與 `specs/audio-generation/spec.md` REMOVED requirement 的 Scenario 三者都會失敗。
- `recommendation`: 把 design 的「英文音檔」改為「音檔」並明確比對條件為檔名集合而非 `en_` 前綴。
- `disposition`: `fix-introduced`
- `introduced_by`: 第 2 輪 Fix Actions 的 V-3（5.2 移除人工刪除舊音檔、全數改由 3.1 負責），使原本被人工刪除掩蓋的 design 措辭落差成為實際漏洞
- 主 agent 已獨立驗證：`ls audio/zh_*.mp3 | wc -l` 為 9，確認該類檔案實際存在；三處措辭落差經 `grep` 確認屬實。

### Suggestion

**R3-2**（原 Suggestion `confidence` 60，`disposition`: `fix-introduced`，`introduced_by`: 第 2 輪 Fix Actions 的 V-5 與同輪主 agent 對 F-3 的更正）
- `layer`: text ／ `location`: `specs/audio-generation/spec.md` Example「段落規則在本書為安全網」；`design.md` 分句 Decision；`tasks.md` 2.1 驗證欄
- `summary`: 三處都把「本書共有 12 處段落邊界，每一處前段皆以句尾標點結束、後段皆以大寫或左引號開頭」當成已確立的事實寫入，spec 更把它寫成規範性的 `SHALL NOT`。但 `story.md` 要到 tasks 1.1 才建立，此宣稱在提案階段無法從 repo 內任何檔案查證；若謄打後實際邊界數不是 12，寫死「12 處」的驗證會誤報失敗，而 spec 的 `SHALL NOT` 會成為一條事後被內容推翻、且隨 archive 進入長期存活 master spec 的需求。
- `recommendation`: spec Example 改為描述規則意圖並移除規範性斷言；tasks 驗證改為「每一處段落邊界」而非寫死數量。

**R3-3**（`confidence` 50，`disposition`: `fix-introduced`，`introduced_by`: 第 2 輪 Fix Actions 的 V-6）
- `layer`: design ／ `location`: `specs/page-navigation/spec.md`「頁碼 tab 列」vs master `openspec/specs/practice-webpage/spec.md` 的 `Child-friendly layout`
- `summary`: 新增的「tab 列 SHALL NOT 換行、SHALL 由自身橫向捲動」與 master 既有且未被本提案修改的 `Child-friendly layout`（`text SHALL remain legible without horizontal scrolling`）在 archive 後會並存於 master spec，措辭上互相牴觸。實質衝突很小（tab 標籤是導覽而非內文），但會留下一組矛盾的需求。
- `recommendation`: 在 tab 列需求上補一句限定橫向捲動僅限 tab 列自身、內文不需橫向捲動即可閱讀。

### Reviewer V 明確判定為誤判而不報告的項目

- `Fail-fast on count mismatch` 的「不產生任何音檔、`story.json` 或 `index.html`」與「檢查通過後立即寫出 `story.json`」不矛盾：產出順序把逐頁檢查排在寫出 `story.json` 之前，兩者互補。
- tab 列自身橫向捲動與 body 不出現水平捲軸不矛盾：捲動侷限在該元素的 scroll container 內。
- `position: sticky` 與同一元素上的 `overflow-x: auto` 不互斥：sticky 失效的條件是祖先具有非 `visible` 的 overflow。
- `grep -n 'TIMINGS'` 不會被 `PAGES` 內小寫的 `timings` 欄位誤觸。

### Reviewer V 對主 agent 自我更正的獨立複核

第 2 輪主 agent 宣稱「本書 12 處段落邊界全部同時滿足標點規則」。Reviewer V 判定**證據不足以查證**：`story.md` 尚未建立，繪本原文未收錄於 repo，artifacts 中可辨識的段落邊界實例只有 p.5 一處（該處與宣稱一致）。同時指出不論真偽，實作同時套用兩條規則，分句結果都正確，受影響的只有寫死「12 處」的驗證指示與 spec 的 Example 措辭 —— 即 R3-2。主 agent 接受此判定：該數字係主 agent 依使用者訊息中的繪本原文於本次工作階段實算而得，而非來自 repo，因此不應以既定事實寫入會被 archive 的 spec。

## Rating

- post-filter cumulative blocking set Critical count: 0
- post-filter cumulative blocking set Warning count: 1
- 非阻塞 triaged finding count: 2
- `critical_gap`: false
- `round_type`: micro
- 理由：V-1 經 Reviewer V 查證為 verified resolution 並離開累積集合，集合一度清空。本輪新增 R3-1 為 `fix-introduced` 且 `confidence` 85 通過 filter，故成為新的阻塞成員，累積阻塞集合為 {R3-1}。R3-2 與 R3-3 的 `confidence` 低於 80，屬非阻塞，仍一併修正。阻塞集合非空，本輪不通過。

## Fix Actions

- **R3-1**：`design.md` 音檔命名 Decision 的「所有不屬於本次產生結果的英文音檔」改為「所有不屬於本次產生結果的音檔」，並明確比對條件為「是否在本次產生的檔名集合中，而非比對 `en_` 前綴」，另補一句「舊繪本的 9 個中文音檔也由這一步清除，不另設人工刪除步驟」，與 `specs/audio-generation/spec.md`、`tasks.md` 3.1 與 5.2、`proposal.md` `## Impact` 四處對齊。修改檔案：`design.md`。
- **R3-2**：`specs/audio-generation/spec.md` 的 Example 改名為「段落規則作為安全網」，內容從斷言本書內容改為以一個構造範例描述規則意圖（前段以句尾標點結束、後段以小寫字母開頭），移除「12 處」與 `SHALL NOT 存在…實例` 的規範性斷言；`design.md` 分句 Decision 改為「就本書已知的段落邊界抽樣而言…預期不會改變本次分句結果」，並明言實際邊界數要到 `story.md` 謄打完成後才能確定；`tasks.md` 2.1 驗證改為「確認**每一處**段落邊界都產生了句界，不寫死邊界數量」。修改檔案：`specs/audio-generation/spec.md`、`design.md`、`tasks.md`。
- **R3-3**：`specs/page-navigation/spec.md`「頁碼 tab 列」補上限定範圍句：橫向捲動僅限 tab 列自身這個導覽元素，句子卡片的英文與中文內文 SHALL NOT 需要橫向捲動即可閱讀，body 亦 SHALL NOT 出現水平捲軸 —— 使其與 master `Child-friendly layout` 在 archive 後不互相牴觸。修改檔案：`specs/page-navigation/spec.md`。

修正後處置：
- 因 fix actions 修改了 design、tasks 與 spec artifacts，已重跑 `cash validate ant-grasshopper-storybook` → Validation passed。
- 已重跑 pre-round mechanical self-check：註解 lint、spec delta 標題身分、每個 requirement 至少一個 scenario、requirement 與 design 標題對 tasks 的交叉引用、孤兒檔清除範圍一致性、「12 處段落邊界」斷言殘留掃描、`globalIdx` 與 `dry-run` 殘留掃描 —— 全數通過。此次自檢未新增發現。
- 本輪 fix actions 未修改 `openspec/changes/` 以外的任何檔案，故不執行 `cash touched` 記錄。
- 本輪無 `未修復：裁判面保護` 記錄。

## Decision

next_round
