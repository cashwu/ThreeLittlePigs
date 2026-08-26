# Cash Propose Review — Round 2

## Reviewer Findings

本輪為 micro round，由單一 Reviewer V 對第 1 輪的累積阻塞集合做差異驗證，並檢查修正傳播與修正引入的新缺陷。

### 累積阻塞集合逐一判定

- **F-1**（Critical，`4114ad5` 未回寫模板）→ **resolved**。Reviewer V 以 `git show --stat 4114ad5` 與逐行比對 `generate_audio.py` 與 `index.html` 確認 design 所列差異與實際檔案逐字相符，且修正落在正確的 artifact（新增 Decision、新增 ADDED 需求含 Example 表、tasks 4.1 附可執行的 `grep` 驗證），不是換句話說。
- **F-2**（Warning，網頁標題未被涵蓋）→ **resolved**。新增 ADDED 需求「網頁標題反映目前的繪本」，design Behavior 與 Acceptance criteria、tasks 4.1 與 5.3 皆已涵蓋，副標刪除的決定一致寫入四個 artifact。

兩個成員皆以「verified resolution」離開累積阻塞集合。

### Warning

**V-1**
- `severity`: Warning
- `confidence`: 80
- `layer`: design
- `location`: `design.md` → `## Decisions` →「tab 切換以顯示/隱藏既有 DOM 實作，並在切頁時停止播放」vs「word boundary 併入 `PAGES`，不保留獨立的全域 `TIMINGS`」
- `summary`: 新 Decision 宣稱「合併之後這個計數器完全消失，錯位在結構上不可能發生」，但未回寫的 tab Decision 仍要求維持 `en-words-<globalIdx>` 這個全域流水 DOM id，跨頁計數器實際上並未消失，兩個 Decision 互相矛盾。
- `recommendation`: 或把 DOM id 改為頁內定位，或改寫結論不宣稱計數器已消失。
- `disposition`: `fix-introduced`
- `introduced_by`: 第 1 輪 Fix Actions 的 F-10（word boundary 併入 `PAGES`）
- 主 agent 已獨立驗證：`design.md` 第 93 行與第 111 行確實並存且互斥。

### Suggestion

以下 `confidence` 落在 [50, 80) 而由 confidence filter 自 Warning 降級，或 reviewer 原本即歸為 Suggestion。全部非阻塞。

**V-2**（原 Warning `confidence` 70 → 降級，`disposition`: `fix-introduced`，`introduced_by`: 第 1 輪 F-6，與 F-3、F-8 的修正交互）
- `layer`: design ／ `location`: `tasks.md` 2.1 驗證欄；`design.md` Failure modes 第 4 點
- `summary`: 移除 `--dry-run` 後 2.1 改以檢視 `story.json` 驗證分句，但 design 的非原子段落明言 `story.json` 要到音檔全部成功後才寫出，使第 2 節的驗證必須先完成第 3、5 節的工作；且該驗證要求的「人工構造測試段落」會改變英文句數而觸發逐頁 fail-fast，導致 `story.json` 根本不會被寫出。
- `recommendation`: 明訂寫出順序為「句數檢查通過 → 立即寫出 `story.json` → 產生音檔 → 寫出 `index.html`」，並移除人工構造測試段落的要求。

**V-3**（原 Warning `confidence` 70 → 降級，`disposition`: `fix-introduced`，`introduced_by`: 第 1 輪 F-4 與 F-8 的交互）
- `layer`: design ／ `location`: `tasks.md` 5.2 vs 3.1；`specs/audio-generation/spec.md` 清除孤兒檔 Scenario
- `summary`: 3.1 與 spec 已要求腳本在成功後刪除所有不屬於本次結果的音檔（含舊的中文音檔與全域流水號音檔），5.2 卻仍把同一刪除寫成人工工作 —— 同一刪除有兩個負責者，5.2 該部分實為空操作，實作者可能因此在腳本中略去清除步驟。
- `recommendation`: 5.2 只刪 `eng.md` 與 `lines.json`，舊音檔部分降為驗證 3.1 是否生效。

**V-4**（`confidence` 50，`disposition`: `fix-introduced`，`introduced_by`: 第 1 輪 F-10）
- `layer`: design ／ `location`: `tasks.md` 4.6 驗證欄
- `summary`: `grep -c 'const TIMINGS' index.html` 為 0 只擋得下「原封不動沿用舊模板」一種寫法，`WORD_TIMINGS`、`let TIMINGS` 等都會讓檢查空轉通過，重蹈第 1 輪 F-7 指出的問題。
- `recommendation`: 改為 `grep -n 'TIMINGS'` 無輸出並補一項正面檢查。

**V-5**（`confidence` 50，`disposition`: `new`）
- `layer`: design ／ `location`: `specs/audio-generation/spec.md` → ADDED「把 story.md 解析為頁與句子」
- `summary`: 第 1 輪 F-3 的修正把段落規則寫進了 `design.md` 與 `tasks.md`，但 spec 這一側仍只有需求文字中的一句，三個 Scenario 與 Example 表全部只示範標點規則，沒有任何一列示範段落邊界。
- `recommendation`: 新增段落邊界的 Scenario 或 Example 列。

**V-6**（`confidence` 50，`disposition`: `fix-introduced`，`introduced_by`: 第 1 輪 F-9）
- `layer`: design ／ `location`: `specs/page-navigation/spec.md`「頁碼 tab 列」；`design.md` tab Decision
- `summary`: 新增的 sticky 要求與既有的「手機寬度下 body SHALL NOT 出現水平捲軸」並存，但沒有任何 artifact 說明 12 個 tab 在手機寬度如何容納；若以換行容納，sticky 的 tab 列會折成 2-3 行並長期占用 viewport 高度。
- `recommendation`: 明訂 tab 列不換行、以橫向捲動容納，並補一行高的驗證。

## Rating

- post-filter cumulative blocking set Critical count: 0
- post-filter cumulative blocking set Warning count: 1
- 非阻塞 triaged finding count: 5
- `critical_gap`: false
- `round_type`: micro
- 理由：第 1 輪的兩個阻塞成員 F-1 與 F-2 皆經 Reviewer V 查證為 verified resolution 並離開累積集合。本輪新增 V-1 為 `fix-introduced` 且 `confidence` 80 通過 filter，故為阻塞成員，累積阻塞集合為 {V-1}。阻塞集合非空，本輪不通過。V-2 至 V-6 的 `confidence` 皆低於 80，經 confidence filter 降級為 Suggestion，屬非阻塞，仍一併修正。

## Fix Actions

- **V-1**：把 DOM id 從全域流水號 `en-words-<globalIdx>` 改為頁內定位 `en-words-p<頁碼兩位>-<頁內序號兩位>`，讓「跨頁計數器消失」的宣稱成立而非只是措辭調整。修改 `design.md` 的 tab Decision（說明改採頁內定位及其理由）、word boundary Decision 的結論句、Implementation Contract 的 Interface（新增 DOM id 條目）；`tasks.md` 4.4 改為交付頁內定位 id 並加上 `document.getElementById('en-words-p12-07')` 的驗證。修改檔案：`design.md`、`tasks.md`。
- **V-2**：`design.md` Implementation Contract 新增明確的產出順序條目（解析與分句 → 逐頁句數檢查 → 寫出 `story.json` → 產生音檔並清除孤兒檔 → 寫出 `index.html`），Failure modes 第 4 點改為「`story.json` 已寫出而 `index.html` 尚未寫出」；`specs/audio-generation/spec.md` 於 `Single source of truth for lines and translations` 加入寫出時機、重跑 Scenario 移除對 `story.json` 的錯誤陳述；`tasks.md` 2.1 驗證改為「執行腳本並在音檔開始產生後即可中止，檢視此時已寫出的 `story.json`」並移除人工構造測試段落的要求。修改檔案：`design.md`、`specs/audio-generation/spec.md`、`tasks.md`。
- **V-3**：`tasks.md` 5.2 改為只刪除 `eng.md` 與 `lines.json`，舊音檔部分改為驗證 3.1 的孤兒檔清除是否生效並註明「若仍存在代表腳本漏了清除步驟」；5.1 括號說明限定為中途失敗的情形。修改檔案：`tasks.md`。
- **V-4**：`tasks.md` 4.6 驗證改為 `grep -n 'TIMINGS' index.html` 無輸出並註明不可只查 `const TIMINGS` 的理由，另補 DevTools 的正面檢查。修改檔案：`tasks.md`。
- **V-5**：`specs/audio-generation/spec.md` 於 ADDED 需求新增 Scenario「段落邊界結束一個句子」與 Example「段落規則在本書為安全網」。修改檔案：`specs/audio-generation/spec.md`。
- **V-6**：`design.md` tab Decision 補明 tab 列不換行、以 `overflow-x: auto` 橫向捲動及其理由；`specs/page-navigation/spec.md`「頁碼 tab 列」補不換行與橫向捲動條款及 Scenario「手機寬度下 tab 列維持一行高」；`tasks.md` 4.3 補一行高與橫向捲動的驗證。修改檔案：`design.md`、`specs/page-navigation/spec.md`、`tasks.md`。

**主 agent 對第 1 輪 F-3 修正的更正**：Reviewer V 的 V-2 促使主 agent 實際驗算本書的段落邊界。以本書 12 處段落邊界逐一套用標點規則，結果為 12 處全部同時滿足標點規則（前段皆以句尾標點結束、後段皆以大寫字母或左引號開頭），**沒有任何一處只有段落規則才會切**。因此第 1 輪 F-3 的修正把段落規則描述為「影響句數的獨立變因」是不正確的：它在本次內容上是安全網而非變因，而 `tasks.md` 2.1 原先要求找出的「只有空行規則才會切」的驗證實例在本書並不存在。已在 `design.md` 的分句 Decision、`specs/audio-generation/spec.md` 的新 Example、`tasks.md` 2.1 三處同步更正此陳述。

修正後處置：
- 因 fix actions 修改了 design、tasks 與 spec artifacts，已重跑 `cash validate ant-grasshopper-storybook` → Validation passed。
- 已重跑 pre-round mechanical self-check：註解 lint、spec delta 標題身分、每個 requirement 至少一個 scenario、requirement 與 design 標題對 tasks 的交叉引用、`globalIdx` 與 `dry-run` 兩個已淘汰識別字的殘留掃描 —— 全數通過。此次自檢未新增發現。
- 本輪 fix actions 未修改 `openspec/changes/` 以外的任何檔案，故不執行 `cash touched` 記錄。
- 本輪無 `未修復：裁判面保護` 記錄。

## Decision

next_round
